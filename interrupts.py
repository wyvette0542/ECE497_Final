#!/usr/bin/env python3
import Adafruit_BBIO.GPIO as GPIO
import time
import subprocess

# setup input and output GPIO
button = "GP1_3"
LED = "GP1_4"
GPIO.setup(button, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)

# map button to led
map = {button: LED}

def updateLED(channel):
	subprocess.call("./grab.sh", shell = True)

print("Running...")

GPIO.add_event_detect(button, GPIO.BOTH, callback=updateLED)

try:
	while True:
		time.sleep(100)

except KeyboardInterrupt:
	print("Cleaning Up")
	GPIO.cleanup()
GPIO.cleanup()

