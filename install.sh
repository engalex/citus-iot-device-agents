#!/bin/sh
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
NC='\033[1;30m' # No Color
DEF='\033[0m' # Default Color

echo -e "${BLUE}INFO: Installing citus-device CLI libraries....${NC}"
cp -r citus/ /usr/sbin/
cp citus-device /usr/sbin/
chmod +x /usr/sbin/citus-device
chmod +x /usr/sbin/citus/*

echo -e "${GREEN}==========================================="
echo -e "| Installed Software Agents successfully. |"
echo -e "===========================================${NC}"
echo -e "${DEF}"