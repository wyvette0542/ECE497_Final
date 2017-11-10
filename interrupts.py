#!/usr/bin/env python3
import os
import Adafruit_BBIO.GPIO as GPIO
import time
from subprocess import call

# setup input and output GPIO
button = "GP1_3"
button_new = "GP1_4"
GPIO.setup(button, GPIO.IN)
GPIO.setup(button_new, GPIO.IN)

def identify(channel):
	state = GPIO.input(channel)
	if state == 0:
		call("./grab.sh")
		time.sleep(5)
		call("./welcome.sh")
		
def addFace(channel):
	flag = False
	state = GPIO.input(channel)
	if state == 0:
		takePicture()
		call(["sudo", "fbi", "-noverbose", "-T", "1", "-a", "anno_label.jpg"])
		call(["./cleanup.sh"])
		time.sleep(5)
		call("./welcome.sh")
		
def takePicture():
	call("./grabber")
	files = next(os.walk("/home/debian/ECE497_Final/database"))[2]
	file_count = len(files)
	print("I have "+str(file_count))
	call(["convert", "*.ppm", str(file_count)+".jpg"])
	name = input("Please enter your name here: ")
	print("You entered " + str(name))
	call(["convert", str(file_count)+".jpg", "-background", "Khaki", "-pointsize", "30", "label:Welcome "+str(name)+"!\nYour name is added.", 
          "-gravity", "Center", "-append", "anno_label.jpg"])
	call(["mv", str(file_count)+".jpg", "database/"])
	
	with open('database/face.dat', 'a') as f:
		f.write(','+name)

call("./welcome.sh")
print("Running...")

GPIO.add_event_detect(button, GPIO.FALLING, callback=identify)
GPIO.add_event_detect(button_new, GPIO.FALLING, callback=addFace)

try:
	while True:
		time.sleep(100)

except KeyboardInterrupt:
	print("Cleaning Up")
	GPIO.cleanup()
GPIO.cleanup()



