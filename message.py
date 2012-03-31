import os
import sys

import badge

DEVICE = "/dev/ttyUSB1"

os.system("stty speed 38400 <" + DEVICE)
f = open(DEVICE, "w")
pkts = badge.build_packets(0x600, badge.message_file(sys.argv[1], speed='5', action=badge.ACTION_HOLD))
for p in pkts:
    f.write(p.format())
f.flush()
f.close()
