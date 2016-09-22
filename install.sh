#!/bin/bash
echo "Installing agents...."
cp -r citus/ /usr/sbin/
cp citus-device /usr/sbin/
chmod +x /usr/sbin/citus-device
chmod +x /usr/sbin/citus/*
mkdir -p $HOME/.agent/
echo "${DEVICE_ID}" >> ${HOME}/.agent/.device-id
echo "${SECRET_KEY}" >> ${HOME}/.agent/.secret-key