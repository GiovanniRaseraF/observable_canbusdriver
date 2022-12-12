import sys
sys.path.append('..')
from canfilereplay import *

if __name__ == "__main__":

    canreplay = canlistenfromfile(
        pathtofile="./toreplay.csv",
        replayfrequency = 0.1
    )

    canreplay.add_listener(motor(desc="motor", on = [0x500, 0x460]))

    print(canreplay)

    canreplay.start()