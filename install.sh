#!/bin/sh
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
NC='\033[1;30m' # No Color
DEF='\033[0m' # Default Color

if ! [ -f /usr/sbin/citus-device ];
then
	echo -e "${BLUE}INFO: Installing citus-device CLI libraries....${NC}"
	cp -r $HOME/citus-iot-device-agents/citus/ /usr/sbin/
	cp $HOME/citus-iot-device-agents/citus-device /usr/sbin/
	chmod +x /usr/sbin/citus-device
	chmod +x /usr/sbin/citus/*
	echo -e "${BLUE}INFO: Installed Software Agents successfully.${NC}"
	echo -e "${DEF}"
else
	echo -e "${YELLOW}WARN: Citus Device Agents has already installed yet.${NC}"
fi

if [ "${INSTALL_ALL}" == "YES" ]; then	
	citus-device activate
fi