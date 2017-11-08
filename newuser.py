#!/usr/bin/env python3
import os
import Adafruit_BBIO.GPIO as GPIO
import time
from subprocess import call

# setup input and output GPIO
button = "GP1_3"
LED = "GP1_4"
GPIO.setup(button, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)

# map button to led
map = {button: LED}

def updateLED(channel):
	state = GPIO.input(channel)
	if state == 0:
		takepicture(str(var))
		appendname(str(var))
		call(["sudo", "fbi", "-noverbose", "-T", "1", "-a", "anno_label.jpg"])
		call(["rm", "*.jpg"])
		
def takepicture(name):
	call("./grabber")
	files = next(os.walk("/home/debian/ECE497_Final/database"))[2]
	file_count = len(files)
	print("I have "+str(file_count))
	call(["convert", "*.ppm", str(file_count)+".jpg"])
	call(["convert", str(file_count)+".jpg", "-background", "Khaki", "-pointsize", "30", "label:Welcome "+name+"!\nYour name is added.", 
          "-gravity", "Center", "-append", "anno_label.jpg"])
	call(["rm", "*.ppm"])
	call(["mv", str(file_count)+".jpg", "database/"])

def appendname(name):
	with open('database/face.dat', 'a') as f:
		f.write(','+name)

var = input("Please enter your name here: ")
print("You entered " + str(var))

print("Running...")

GPIO.add_event_detect(button, GPIO.FALLING, callback=updateLED)

try:
	while True:
		time.sleep(100)

except KeyboardInterrupt:
	print("Cleaning Up")
	GPIO.cleanup()
GPIO.cleanup()

