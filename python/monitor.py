#!/usr/bin/python3 -I

import urllib3
import os
import psutil
import signal
import daemon
import sys
import threading
from time import sleep
from telegram.ext import Updater, CommandHandler
import logging
from daemon.pidfile import TimeoutPIDLockFile
import random
import string
import subprocess
import yaml

# Default variables
token = None


def readConf(path="/etc/check/config.yml"):
    try:
        with open(path, 'r') as ymlfile:
            return yaml.load(ymlfile)
    except IOError:
        sys.stderr.write(
            "Error: Configuration file %s does not appear to exist."
            % path)
        sys.exit(1)
    except ImportError:
        sys.stderr.write(
            "Error: Configuration file %s is not valid." % path)
        sys.exit(1)


def getLogger():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
    logger = logging.getLogger(cfg['MONITOR_NAME'])
    handler = logging.handlers.SysLogHandler(address='/dev/log')
    logger.addHandler(handler)
    return logger


cfg = None
logger = None
check_thread = None
updater = None
pid = None

if (
    (len(sys.argv) == 3) and
    (sys.argv[2] in ['start', 'stop', 'reload', 'status'])
):
    cfg = readConf(sys.argv[1])
    updater = Updater(token=cfg['TOKEN'], use_context=True)
    pid = TimeoutPIDLockFile(cfg['PIDFILE'], cfg['LOCK_WAIT_TIMEOUT'])
    if sys.argv[2] == 'stop':
        if pid.is_locked():
            pidNumber = pid.read_pid()
            os.kill(pidNumber, signal.SIGHUP)
            sleep(15)
            if psutil.pid_exists(pidNumber):
                os.kill(pidNumber, signal.SIGTERM)
                sleep(5)
                if psutil.pid_exists(pidNumber) or pid.is_locked():
                    sys.stderr.write(
                        cfg['MONITOR_NAME'] + " Bot can't be stopped")
                    sys.exit(1)
        sys.exit(0)
    elif sys.argv[2] == 'reload':
        if pid.is_locked():
            os.kill(pid.read_pid(), signal.SIGUSR1)
        sleep(5)
        sys.exit(0)
    elif sys.argv[2] == 'status':
        if pid.is_locked():
            sys.stdout.write(
                "%s Bot Active with PID: %s,%s" %
                (cfg['MONITOR_NAME'], pid.read_pid(), pid.is_locked()))
            sys.exit(0)
        else:
            sys.stdout.write(cfg['MONITOR_NAME'] + " Bot No Active")
            sys.exit(1)
    elif sys.argv[2] != 'start':
        sys.stderr.write(
            "Command must be %s CONFIGFILE.yml [start|stop|status|reload]\n"
            % sys.argv[0])
        sys.stderr.write(
            "If is used without arguments then start is selected\n" %
            sys.argv[0])
        sys.exit(1)
else:
    sys.stderr.write(
        "Command must be %s CONFIGFILE.yml [start|stop|status|reload]\n"
        % sys.argv[0])
    sys.exit(1)

if pid.is_locked() and not pid.i_am_locking():
    logging.warning("%s is locked, but not by me" % cfg['PIDFILE'])
    sys.exit(1)


def generateToken(len=8):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(len))


def monitor():
    try:
        http = urllib3.PoolManager()
        response = http.request('GET', cfg['MONITOR_URL'])
        if response.status != 200:
            return False
        return True
    except urllib3.exceptions.HTTPError:
        return False


def program_cleanup(signum, frame):
    logger.warning(cfg['MONITOR_NAME'] + " - SIGTERM received - CleanUp")
    check_thread.noStop = False
    check_thread.join()
    logger.warning(cfg['MONITOR_NAME'] + " - SIGTERM received - Close Monitor")
    updater.stop()
    logger.warning(
        cfg['MONITOR_NAME'] + " - SIGTERM - Close Telegram Connection")
    sys.exit(0)


def reload_program_config(signum, frame):
    global cfg, updater
    logger.warning(cfg['MONITOR_NAME'] + " - SIGUSR1 received - Reload")
    check_thread.noStop = False
    check_thread.join()
    sleep(15)
    oldToken = cfg['TOKEN']
    cfg = readConf()
    if oldToken != cfg['TOKEN']:
        updater.stop()
        updater = Updater(token=cfg['TOKEN'], use_context=True)
        dispatcher = updater.dispatcher
        start_handler = CommandHandler('start', start)
        dispatcher.add_handler(start_handler)
        status_handler = CommandHandler('status', status)
        dispatcher.add_handler(status_handler)
        token_handler = CommandHandler('token', token)
        dispatcher.add_handler(token_handler)
        restart_handler = CommandHandler('restart', restart)
        dispatcher.add_handler(restart_handler)
    check_thread.noStop = False
    check_thread.join()
    check_thread.start()
    sys.exit(0)


def end_program(signum, frame):
    logger.warning(cfg['MONITOR_NAME'] + " - SIGHUP - Terminate")
    check_thread.noStop = False
    check_thread.join()
    logger.warning(cfg['MONITOR_NAME'] + " - SIGHUP - Close Monitor")
    updater.stop()
    logger.warning(
        cfg['MONITOR_NAME'] + " - SIGHUP - Close Telegram Connection")
    sys.exit(0)


def start(update, context):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))
    if monitor():
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=cfg['MONITOR_NAME'] + ". Status: OK")
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=cfg['MONITOR_NAME'] + ". Status: ERROR")


def status(update, context):
    if monitor():
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=cfg['MONITOR_NAME'] + " Status: OK")
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=cfg['MONITOR_NAME'] + " Status: ERROR")


def token(update, context):
    global token
    token = generateToken()
    logger.info(cfg['MONITOR_NAME'] + " - Generate token: %s" % token)
    context.bot.send_message(chat_id=cfg['CHAT_ID'], text="%s" % token)


def restart(update, context):
    global token
    msgText = update.effective_message.text
    if token is not None and msgText == "/restart %s" % token:
        logger.info(cfg['MONITOR_NAME'] + " - Restart: %s" % msgText)
        subprocess.call(cfg['CMD'], shell=True)
        update.message.reply_text("Restart Completed")
    else:
        logger.info(cfg['MONITOR_NAME'] + " - Incorrect Token")
        update.message.reply_text("Incorrect Token")
    token = None


def monitorProc(updater, logger):
    t = threading.currentThread()
    t.noStop = True
    while getattr(t, "noStop", True):
        sleep(10)
        if not monitor():
            updater.bot.send_message(
                chat_id=cfg['CHAT_ID'],
                text=cfg['MONITOR_NAME'] + " Status: ERROR")
            sleep(540)
    logger.info(cfg['MONITOR_NAME'] + " - Monitor Stopped")


def do_main_program(logger, updater):
    while True:
        updater.start_polling()
        sleep(1)


context = daemon.DaemonContext(
    # stdout=sys.stdout,
    stderr=sys.stderr,
    chroot_directory=None,
    working_directory='/tmp',
    umask=0o002,
    pidfile=pid,
    )

context.signal_map = {
    signal.SIGTERM: program_cleanup,
    signal.SIGHUP: end_program,
    signal.SIGUSR1: reload_program_config,
    }

with context:
    logger = getLogger()
    logger.info(cfg['MONITOR_NAME'] + " starting")
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    status_handler = CommandHandler('status', status)
    dispatcher.add_handler(status_handler)
    token_handler = CommandHandler('token', token)
    dispatcher.add_handler(token_handler)
    restart_handler = CommandHandler('restart', restart)
    dispatcher.add_handler(restart_handler)
    logger.info(cfg['MONITOR_NAME'] + " main loop")
    check_thread = threading.Thread(
        target=monitorProc, args=(updater, logger, ))
    check_thread.start()
    do_main_program(logger, updater)
