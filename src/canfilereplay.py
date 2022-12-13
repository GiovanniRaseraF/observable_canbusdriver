#
# Author: Giovanni Rasera
# Link: https://www.github.com/GiovanniRaseraF
#
# Desciption:
#   file replayer 
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

# File replay feature
class canlistenfromfile(threading.Thread):
    file = None
    pathtofile = ""
    __listenersdict = {}
    freq = 1.0

    # @param replayfrequency: seconds
    def __init__(self, pathtofile: str, replayfrequency = 1.0):
        try:
            self.file = open(file=pathtofile)        
        except:
            log.error("cannot open file for replay")
            exit(1)
        self.pathtofile = pathtofile
        self.freq = replayfrequency

        threading.Thread.__init__(self)

    # TODO: implement timings
    def read(self) -> None:
        if self.file == None: return

        line = self.file.readline()
        vals = line.split(" ")

        id = int(vals[0], 16)
        data = int(vals[1], 16).to_bytes(8, "big") 

        # parse
        if id in self.__listenersdict:
            for l in self.__listenersdict[id]:
                l.update(data, id)

    # Listeners
    def add_listener(self, new_listener: listener) -> bool:
        for on in new_listener.on:
            if on not in self.__listenersdict:
                self.__listenersdict[on] = []
                self.__listenersdict[on].append(new_listener)
            else:
                self.__listenersdict[on].append(new_listener)

        log.info("added new listener to notification list")

    def __str__(self):
        ret = f"canreplay file: {self.pathtofile}\n"

        for key, val in self.__listenersdict.items():
            ret += f" - {hex(key)} : "
            for l in val:
                ret += f"{l.description}, "
            ret += "\n"

        return ret

    def run(self):
        while(True):
            self.read()
            time.sleep(self.freq)
    
    def __del__(self):
        self.file.close()