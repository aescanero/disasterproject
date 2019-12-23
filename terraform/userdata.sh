#!/bin/sh
sudo systemctl stop unattended-upgrades
sudo apt-get --purge -y remove unattended-upgrades
