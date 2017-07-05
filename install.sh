#!/bin/sh
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
NC='\033[1;30m' # No Color
DEF='\033[0m' # Default Color

echo -e "${BLUE}INFO: Installing citus-device CLI libraries....${NC}"
cp -r $HOME/citus-iot-device-agents/citus/ /usr/local/bin/
cp $HOME/citus-iot-device-agents/citus-device /usr/local/bin/
chmod +x /usr/local/bin/citus-device
chmod +x /usr/local/bin/citus/*
ln -s /usr/local/bin/citus-device /usr/bin/citus-device
echo -e "${DEF}"

if [ "${INSTALL_ALL}" = "YES" ]; then
	citus-device activate
fi