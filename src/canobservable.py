#
# Author: Giovanni Rasera
# Link: https://www.github.com/GiovanniRaseraF
#
# Description:
#   Module to provide ad observable can bus interface with automatic detection
#   and connection to the canbus socket in linux
#   
#   Replay feature form csv file
#   TODO: replay with timings
#

import can
import sys
import os
import time
import threading
import struct
import binascii
from listener import listener, motor
import logging as log
import pathlib

def trytoload():
    for i in range(0, 4):
        os.system(f"sudo /sbin/ifconfig can{i} down 2> /dev/null")
        os.system(f"sudo /sbin/ip link set can{i} up type can bitrate 250000 2> /dev/null") 
        os.system(f"sudo /sbin/ifconfig can{i} up 2> /dev/null")

# Read canbus from linux socket
class canlisten(threading.Thread):
    __listenersdict = {} 
    canbus = None
    
    # constructor RAII
    def __init__(self, interface = "can", baudrate = 25000):
        if interface == "replay":
            threading.Thread.__init__(self)
            return

        # try load
        if interface == "can": trytoload()

        log.info("checking can inteface presence")

        # test using ifconfig the presence of can interface
        os.system(f"sudo /sbin/ifconfig | grep {interface}| cut -c1-4 > can.txt")
        canfile = open("can.txt", "r")
        caninterface = canfile.readline()
        canfile.close()
        # interface in the first line
        caninterface = caninterface.strip() 

        # check for prosence
        if caninterface == "":
            log.error("no can interfaces")
            exit(1)

        log.info(f"interface found, try to connect to: {caninterface}")
        
        os.system(f"sudo /sbin/ifconfig {caninterface} down 2> /dev/null")
        os.system(f"sudo /sbin/ip link set {caninterface} up type can bitrate {baudrate} 2> /dev/null")
        os.system(f"sudo /sbin/ifconfig {caninterface} up 2> /dev/null")
       
        try:
            self.canbus = can.interface.Bus(channel=caninterface, bustype="socketcan")
        except:
            log.error(f"cannot connect to: {caninterface}")
            exit(1)
       
        log.info(f"success connection to: {caninterface}")

        # threading feature
        threading.Thread.__init__(self)

    """
    Add listeners to the dict
    """
    def add_listener(self, new_listener: listener) -> bool:
        for on in new_listener.on:
            if on not in self.__listenersdict:
                self.__listenersdict[on] = []
                self.__listenersdict[on].append(new_listener)
            else:
                self.__listenersdict[on].append(new_listener)

        log.info("added new listener to notification list")

        return True

    def read(self) -> None:
        message = self.canbus.recv()
        id = message.arbitration_id
        data = message.data

        if id in self.__listenersdict:
            for l in self.__listenersdict[id]:
                l.update(data, id)

    def __str__(self):
        ret = f"interface: {self.canbus.channel_info}\n"

        for key, val in self.__listenersdict.items():
            ret += f" - {hex(key)} : "
            for l in val:
                ret += f"{l.description}, "
            ret += "\n"

        return ret 

    def run(self):
        log.info("started can thread")

        while(True):
            self.read()

    def close():
        log.info("closing can interface")
        # TODO: closing 

   
# Main for debug
if __name__ == "__main__":
    # loggin level
    log.basicConfig(level=log.INFO) 
    log.info("module test for CAN Listener and Notifyer")

    # connect
    canbus = canlisten(
        interface   = "can",
        baudrate    = 250000
    )

    # listening the motor at this channels
    m = motor("motor", [0x500, 0x501, 0x502, 0x503, 0x504, 0x505, 0x506, 0x700, 0x701, 0x702])
    canbus.add_listener(m)

    # log
    print(canbus)
    input("PRESS RETURN to continue :>")

    # create can thread
    canbus.start()
    canbus.join()
    # close
    # Auto disconnection
    
