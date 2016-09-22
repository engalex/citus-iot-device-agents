#!/bin/sh
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}INFO: Installing agents....${NC}"
cp -r citus/ /usr/sbin/
cp citus-device /usr/sbin/
chmod +x /usr/sbin/citus-device
chmod +x /usr/sbin/citus/*

echo -e "${BLUE}INFO: Installing docker engine...${NC}"
curl -sSL https://get.docker.com | sh
echo $(docker -v)
echo -e "${GREEN}=================================
echo -e | INFO: Installed successfully. |
echo -e =================================${NC}"