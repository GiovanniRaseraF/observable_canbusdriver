import sys
sys.path.append('..')
from canobservable import *
from listener import *

# Can bus sniffer
# Chosing to sniff 4 channels
sniffer1 = sniffer(
    on      = {0x100, 0x500, 0x501, 0x502},
    desc    = "sniffer 1"
)

# setup canbus unknown port
canbus = canlisten(
    interface   = "can",
    baudrate    = 250000,
)

# listeners list
canbus.add_listener(sniffer1)

# info
print(canbus)

# start thread
canbus.start()
