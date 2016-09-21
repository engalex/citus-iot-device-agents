#!/bin/bash
echo "Installing agents...."
sudo cp -r citus/ /usr/sbin/
sudo cp citus-device /usr/sbin/
sudo chmod +x /usr/sbin/citus-device
sudo chmod +x /usr/sbin/citus/*
mkdir -p $HOME/.agent/
echo "${DEVICE_ID}" >> ${HOME}/.agent/.device-id
echo "${SECRET_KEY}" >> ${HOME}/.agent/.secret-key