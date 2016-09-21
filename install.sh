#!/bin/bash
echo "Installing agents...."
sudo cp -r citus/ /usr/sbin/
sudo cp citus-device /usr/sbin/
sudo chmod +x /usr/sbin/citus-device
sudo chmod +x /usr/sbin/citus/*