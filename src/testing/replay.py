import sys
sys.path.append('..')
from canfilereplay import *

if __name__ == "__main__":
    log.basicConfig(level=log.INFO)
    log.info("canreplay with 0.01s wait for data and file looping enabled")

    canreplay = canlistenfromfile(
        pathtofile="./toreplay.csv",
        replayfrequency = 0.01,
        loopfile = True
    )

    canreplay.add_listener(motor(desc="motor", on = [0x500, 0x460]))
    canreplay.add_listener(motor(desc="battery", on = [0x500]))

    print(canreplay)

    canreplay.start()
