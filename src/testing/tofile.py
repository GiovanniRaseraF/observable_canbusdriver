import sys
sys.path.append('..')
from canobservable import *
from listener import *
import time
import threading
from threading import Thread 

# battery example, connecting and transforming data
class hpbattery(listener, Thread):
    bat_TotalVoltage = 0				# V
    bat_TotalCurrent = 0				# A
    bat_BatteryTemperature = 0			# °C
    bat_BMSTemperature = 0				# °C
    bat_Power = 0 						# KW,
    bat_TimeToEmpty = 0					# min
    bat_SOC = 0							# %
    bat_auxBatteryVoltage = 0			# V
    bat_status = 0						# bitfield
    bat_warnings = 0					# bitfield
    bat_faults = 0						# bitfield

    def __init__(self):
        listener.on = [0x505, 0x506]
        listener.description = "hpbattery"
        # Threading start
        threading.Thread.__init__(self)

    def update(self, data: bytes, channel: int) -> None:
        if channel == 0x505:
            self.bat_TotalVoltage       = (float(int.from_bytes(data[0 : 2], byteorder="big", signed=True)) / 10.0)
            self.bat_TotalCurrent       = (float(int.from_bytes(data[2 : 4], byteorder="big", signed=True)) / 10.0)
            self.bat_BatteryTemperature = int.from_bytes(data[4 : 5], byteorder="big", signed=False)
            self.bat_BMSTemperature     = int.from_bytes(data[5 : 6], byteorder="big", signed=False)
            self.bat_SOC                = int.from_bytes(data[6 : 7], byteorder="big", signed=False)

        if channel == 0x506:
            self.bat_faults             = '{0:X}'.format(int.from_bytes(data[0 : 1], byteorder="little", signed=False))
            self.bat_warnings           = '{0:X}'.format(int.from_bytes(data[1 : 2], byteorder="little", signed=False))
            self.bat_status             = '{0:X}'.format(int.from_bytes(data[2 : 3], byteorder="little", signed=False))
            self.bat_Power              = (float(int.from_bytes(data[3 : 5], byteorder="big", signed=True)) / 10.0)
            self.bat_TimeToEmpty        = int.from_bytes(data[5 : 7], byteorder="big", signed=False)
            self.bat_auxBatteryVoltage  = (float(int.from_bytes(data[7 : 8], byteorder="big", signed=False)) / 10.0)
    
    def run(self):
        while(True):
            time.sleep(1)

            print(f"{self.bat_TotalVoltage}")

if __name__ == "__main__":
    hpbatt = hpbattery()

    canbus = canlisten(
        interface= "can",
        baudrate= 25000
    )
    canbus.add_listener(hpbatt)

    canbus.start()
    hpbatt.start()

    canbus.join()
    hpbatt.join()
    