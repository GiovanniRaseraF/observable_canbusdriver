# Observable CAN BUS Driver
- This is a linux "driver" that can be used to listen to can bus events
- The notification follows the Observer design pattern
- The canlistener runs in a separate thread
- Connection to the can is done following RAII

# usage
```python
# motor example
from listener import listener, motor
from canobservable import canlisten

# connect to canbus interface
canbus = canlisten(
    interface   = "can",
    baudrate    = 250000
)

# listening the motor at this channels
m = motor(
    desc        = "motor", 
    on          = [0x00, 0x11, 0x55, 0x88]
)

canbus.add_listener(m)

# log
print(canbus)
input("PRESS RETURN to continue :>")

# create can thread
canbus.start()
```

# run
```sh
sudo pip install python-can
sudo python3 main.py 
```
