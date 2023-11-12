import pycromanager
import time
from datetime import datetime
import os

mm_core = pycromanager.Core()

device_name = "LaserSource:Lumencor_Celesta:0x2D3740AF"
shutter_name = ""

mm_core.set_property(device_name, "VIOLET", "0")
mm_core.set_property(device_name, "RED", "0")
mm_core.set_property(device_name, "GREEN", "0")

filename = os.path.expanduser("~/Desktop/timing.txt")

while True:

    t0 = datetime.now()
    # turn on the laser for 0.05 seconds and set the intensity to 155 to align posh acquirement
    mm_core.set_property(device_name, "State", "1")

    mm_core.set_property(device_name, "VIOLET", "1")
    mm_core.set_property(device_name, "VIOLET_Intensity", "155")
    time.sleep(0.03)

    # Record the time and turn off the violet laser
    t1 = datetime.now()
    mm_core.set_property(device_name, "VIOLET", "0")
    time.sleep(0.3)

    # Turn on the green laser and wait for 0.3 seconds and set the intensity to 500
    mm_core.set_property(device_name, "GREEN", "1")
    mm_core.set_property(device_name, "GREEN_Intensity", "500")
    time.sleep(0.2)

    # Record the time and turn off the green laser
    t2 = datetime.now()
    mm_core.set_property(device_name, "GREEN", "0")
    time.sleep(0.3)

    # Turn on the red laser and wait for 0.5 seconds
    mm_core.set_property(device_name, "RED", "1")
    mm_core.set_property(device_name, "RED_Intensity", "300")
    time.sleep(0.333)

    # Turn off the red laser

    mm_core.set_property(device_name, "RED", "0")
    time.sleep(0.5)
    # Write the timing to the file
    with open(filename, "a") as f:
        f.write(str((t0, t1, t2)) + "\n")