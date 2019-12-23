#!/bin/sh
sudo apt-get update
sudo systemctl stop unattended-upgrades
sudo apt-get --purge -y remove unattended-upgrades
sudo apt-get install -y software-properties-common
sudo apt-add-repository -y ppa:ansible/ansible
sudo apt-get update
sudo apt-get install -y ansible
sudo apt-get install -y python-pip python-netaddr curl
curl -LSs https://github.com/kubernetes-sigs/kubespray/archive/master.tar.gz|tar --no-overwrite-dir -C /opt -xz

