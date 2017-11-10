#!/usr/bin/env python3
import http.client, urllib, base64, json
import os
import Adafruit_BBIO.GPIO as GPIO
import time
from subprocess import call

subscription_key = '7ffe7a3ee1844bc2aa3211c4f02bbc55'
uri_base = 'eastus.api.cognitive.microsoft.com'
# Request headers.
headers_octet = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': subscription_key,
}

headers_json = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': subscription_key,
}

# Request parameters.
params = urllib.urlencode({
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': '',
})

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
	body1 = ""
	filename = '/home/debian/ECE497_Final/'+str(file_count)+'.jpg'
	f = open(filename, "rb")
	body1 = f.read()
	f.close()
	try:
		# Execute the REST API call and get the response.
		conn = http.client.HTTPSConnection('eastus.api.cognitive.microsoft.com')
		conn.request("POST", "/face/v1.0/detect?%s" % params, body1, headers_octet)
		response1 = conn.getresponse()
		data1 = response1.read()
		print("I'm here!")
		
		# 'data' contains the JSON data. The following formats the JSON data for display.
		parsed1 = json.loads(data1)
		# print ("Response:")
		# # print (json.dumps(parsed, sort_keys=True, indent=2))
		# print(parsed1[0]['faceId'])
		# id1 = parsed1[0]['faceId']
		conn.close()
	except Exception as e:
		call(["convert", str(file_count)+".jpg", "-background", "Khaki", "-pointsize", "30", "label:Sorry we can't find your face\nPlease make sure your face is clear \nand try again!", 
		         "-gravity", "Center", "-append", "anno_label.jpg"])
		# call(["sudo", "fbi", "-noverbose", "-T", "1", "-a", "anno_label.jpg"])
		# call("./cleanup.sh")

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



