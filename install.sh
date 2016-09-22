#!/bin/bash
echo "Installing agents...."
cp -r citus/ /usr/sbin/
cp citus-device /usr/sbin/
chmod +x /usr/sbin/citus-device
chmod +x /usr/sbin/citus/*