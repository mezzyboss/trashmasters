import subprocess
import io
import os
from nanpy import (ArduinoApi, SerialManager)
from time import sleep
from nanpy import Servo

subprocess.call(['/home/pi/capture.sh'])
print("Processing Image, Thank You")

#This is the setup code for the arduino
ledPaper = 7
ledPlastic = 6
ledTrash = 5
foundPaper = False
foundPlastic = False

#Attempts to connect to the arduino (ensures a proper connection)
try:
    connection = SerialManager()
    a = ArduinoApi(connection = connection)
except:
    print("Failed to connect to the Arduino")

#Setup pins (Same as the Arduino IDE)
a.pinMode(ledPaper, a.OUTPUT)
a.pinMode(ledPlastic,a.OUTPUT)
a.pinMode(ledTrash,a.OUTPUT)

#Imports the Google cloud client library
from google.cloud import vision
from google.cloud.vision import types

#Instantiates a client
client = vision.ImageAnnotatorClient()

#The name of the image file
file_name = '/home/pi/Pictures/image.jpg'

#Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

#Performs lable detection
response = client.label_detection(image=image)
labels = response.label_annotations

print('Labels:')
for label in labels:
    print(label.description)



#Code to actually determine which Leds should be on from labels
for label in labels:
    if(label.description == "Paper"):
        foundPaper = True
    if(label.description == "Plastic" or label.description == "Bottle" or label.description == "Plastic bottle"):
        foundPlastic = True

if(foundPaper == True):
    print("Paper has been detected!")
   # a.digitalWrite(ledPaper,a.HIGH)
   # sleep(5)
   # a.digitalWrite(ledPaper,a.LOW)
    
    servoPaper = Servo(10)
   #Servo code Paper Servo
    for x in range(0,100):
        servoPaper.write(x)
        sleep(0.01)
   
    sleep(5)
    for x in range(100,0,-1):
        servoPaper.write(x)
        sleep(0.01)

elif(foundPlastic == True):
    print("Plastic has been detected!")
   # a.digitalWrite(ledPlastic,a.HIGH)
   # sleep(5)
   # a.digitalWrite(ledPlastic,a.LOW)
    
    servoPlastic = Servo(3)
    #Servo code Plastic Servo
    for x in range(0,100):
        servoPlastic.write(x)
        sleep(0.01)
    
    sleep(5)
    for x in range (100,0,-1):
        servoPlastic.write(x)
        sleep(0.01)
    
else:
    print("Trash is neither Paper nor Plastic!")
   # a.digitalWrite(ledTrash,a.HIGH)
   # sleep(5)
   # a.digitalWrite(ledTrash,a.LOW)
    
    servoTrash = Servo(11)
   #Servo code trash servo
    for x in range(0,100):
        servoTrash.write(x)
        sleep(0.01)
   
    sleep(5)
    for x in range(100,0,-1):
        servoTrash.write(x)
        sleep(0.01)
