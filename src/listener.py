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
        listener.on = on
        listener.desctiption = desc 

    def update(self, data: bytes, channel: int) -> None:
        print(f"{channel} : {data}")   