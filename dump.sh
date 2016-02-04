#!/bin/bash

MMC_HOST_NAME=mmc0
SYS_CLASS_PATH=`ls  -d /sys/class/mmc_host/${MMC_HOST_NAME}/mmc*`
MMC_CARD_NAME=`basename $SYS_CLASS_PATH`
DEBUG_PATH="/sys/kernel/debug/${MMC_HOST_NAME}/${MMC_CARD_NAME}"

echo -e "CID:"
if [ -e "${SYS_CLASS_PATH}/cid" ]
then
	cat "${SYS_CLASS_PATH}/cid" | ./emmc5_reg_reader.py -i
else
	echo "No CID found"
fi

echo -e "\nCSD:"
if [ -e "${SYS_CLASS_PATH}/csd" ]
then
	cat "${SYS_CLASS_PATH}/csd" | ./emmc5_reg_reader.py -s
else
	echo "No CSD found"
fi

echo -e "\nEXT_CSD:"
if [ -e "${DEBUG_PATH}/ext_csd" ]
then
	cat "${DEBUG_PATH}/ext_csd" | ./emmc5_reg_reader.py -e
else
	echo "No EXT CSD found"
fi

