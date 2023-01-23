#
# Author: Giovanni Rasera
# Link: https://www.github.com/GiovanniRaseraF
#
# Desciption:
#   Interface for canobservable
#

import os
import sys 
import time

class listener():
    # short description, MAX 1 word 
    description = ""
    on: list

    def update(self, data: bytes, channel: int) -> None:
        # Here you can implement data parsing
        pass

# motor example
class motor(listener):
    def __init__(self, desc: str, on: list):
        self.on = on
        self.description = desc 

    def update(self, data: bytes, channel: int) -> None:
        print(f"{channel} : {data}") 

# generic sniffer 
class sniffer(listener):
    def __init__(self, desc: str, on: list):
        self.on = on
        self.description = desc 

    def update(self, data: bytes, channel: int) -> None:
        print(f"{channel} : {data}") 