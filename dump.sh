#!/bin/bash

echo -e "CID:"
cat /sys/class/mmc_host/mmc0/mmc0\:0001/cid | ./emmc5_reg_reader.py -i

echo -e "\nCSD:"
cat /sys/class/mmc_host/mmc0/mmc0\:0001/csd | ./emmc5_reg_reader.py -s

echo -e "\nEXT_CSD:"
cat /sys/kernel/debug/mmc0/mmc0\:0001/ext_csd | ./emmc5_reg_reader.py -e

