#!/usr/bin/env python2
import os, csv
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-i", "--cid", action="store_const", const=1, dest="target",
        help="parse cid value")
parser.add_option("-s", "--csd", action="store_const", const=2, dest="target",
        help="parse csd value")
parser.add_option("-e", "--ecsd", action="store_const", const=3, dest="target",
        help="parse ext_csd value")

(opts, args) = parser.parse_args()

if not opts.target:
    parser.error("No option provided")

# Define number of bytes in each register
cid_bits = 128
csd_bits = 126
ecsd_bytes = 512


# Define path to map files
path_cid_map = "./map/cid.csv"
path_csd_map = "./map/csd.csv"
path_ecsd_map = "./map/ecsd.csv"

# Define path to result files
path_result = "./result/"

# Get device specific information
#vendor = raw_input("Please enter the eMMC vendor: ")
#capacity = raw_input("Please enter the eMMC capacity: ")

# Wait for devices
print "Wait for device..."
#os.popen('adb wait-for-device')
#dsn = os.popen('adb devices').readlines()[1].split('\t')[0]
#print "Device " + dsn + " detected"

val = raw_input()

# Load register map
f_cid_map = open(path_cid_map, 'r')
f_csd_map = open(path_csd_map, 'r')
f_ecsd_map = open(path_ecsd_map, 'r')

# Create result file
if not os.path.exists(path_result):
    os.popen("mkdir " + path_result)
f_result = open(path_result + "vendor" + "_" + "cap" + ".csv", 'wb')
result_writer = csv.writer(f_result)


if opts.target == 1:
    # Parse CID. Basic unit is bit, MSB first
    print "Parsing CID value..."
    pos_cur = 0
    val_cid_bin = format(int(val, 16), '0128b')
    result_writer.writerow(('', '', 'CID'))
    for line in f_cid_map:
        tokens = line[:-1].split(",")
        try:
            size_cur = int(tokens[2], 10)
            # Peel off the right number of bits
            value_cur = int(val_cid_bin[pos_cur : pos_cur + size_cur], 2)
            value_cur = format(value_cur, '#x')
            pos_cur = pos_cur + size_cur
        except ValueError:
            value_cur = ""    
        result_writer.writerow((tokens[0], tokens[1], tokens[2], tokens[3], value_cur))

if opts.target == 2:
    # Parse CSD. Basic unit is bit, MSB first
    print "Parsing CSD value..."
    pos_cur = 0
    val_csd_bin = format(int(val, 16), '0128b')
    result_writer.writerows(('', ''))
    result_writer.writerow(('', '', 'CSD'))
    for line in f_csd_map:
        tokens = line[:-1].split(",")
        try:
            size_cur = int(tokens[2], 10)
            # Peel off the right number of bytes
            value_cur = int(val_csd_bin[pos_cur : pos_cur + size_cur], 2)
            value_cur = format(value_cur, '#x')
            pos_cur = pos_cur + size_cur
        except ValueError:
            value_cur = ""
        result_writer.writerow((tokens[0], tokens[1], tokens[2], tokens[3], tokens[4], value_cur))


if opts.target == 3:
    # Parse ext-CSD. Basic unit is byte. LSB first
    print "Parsing ext-CSD value..."
    pos_cur = ecsd_bytes*2
    result_writer.writerows(('', ''))
    result_writer.writerow(('', '', 'EXT-CSD'))
    for line in f_ecsd_map:
        tokens = line[:-1].split(",")
        # One line started with "Modes Segment" does not have this field
        try:
            size_cur = int(tokens[2], 10)
            value_cur = ""
            for i in range(0, size_cur):
                pos_cur = pos_cur - 2
                value_cur = value_cur + val[pos_cur: pos_cur + 2]
        except ValueError:
            value_cur = ""
        # Peel off the right number of bytes
        result_writer.writerow((tokens[0], tokens[1], tokens[2], tokens[3], tokens[4], value_cur))


# Close all the files at last
f_cid_map.close()
f_csd_map.close()
f_ecsd_map.close()
f_result.close()
print "Done!"
