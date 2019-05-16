#!/usr/bin/env python

import os
import time
import sys
import signal
import RPi.GPIO as GPIO
import VL53L1X


print("""distance.py

Display the distance read from the sensor.

Press Ctrl+C to exit.

""")


"""
Open and start the VL53L1X ranging sensor
"""

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)

GPIO.output(16, GPIO.LOW)
GPIO.output(23, GPIO.LOW)
time.sleep(0.5)

GPIO.output(16, GPIO.HIGH)
time.sleep(0.5)

tof = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
tof.open() # Initialise the i2c bus and configure the sensor
tof.change_address(0x2b)
tof.close()
tof.open()
tof.start_ranging(1) # Start ranging, 1 = Short Range, 2 = Medium Range, 3 = Long Range

GPIO.output(23, GPIO.HIGH)
time.sleep(0.5)

tof2 = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
tof2.open() # Initialise the i2c bus and configure the sensor
tof2.start_ranging(1) # Start ranging, 1 = Short Range, 2 = Medium Range, 3 = Long Range

running = True

def exit_handler(signal, frame):
    global running
    running = False
    tof.stop_ranging() # Stop ranging
    tof2.stop_ranging() # Stop ranging
    print()
    sys.exit(0)

signal.signal(signal.SIGINT, exit_handler)

while running:
    distance_in_mm = tof.get_distance() # Grab the range in mm
    print("tof Distance: {}mm".format(distance_in_mm))
    distance_in_mm = tof2.get_distance() # Grab the range in mm
    print("tof2 Distance: {}mm".format(distance_in_mm))
    time.sleep(1)

