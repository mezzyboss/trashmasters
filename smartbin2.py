import subprocess
import RPi.GPIO as GPIO
import io
import os
import bluetooth
import mysql.connector
from google.cloud import vision
from google.cloud.vision import types

GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Need to establish the bluetooth socket connection with
#the bluetooth modlue connected to the Arduino
bluetooth_addr = "00:14:03:05:5A:4B"
bluetooth_port = 1
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((bluetooth_addr,bluetooth_port))

#mySQL database connection
mydb = mysql.connector.connect(
  host="192.168.1.5",
  user="piotr",
  password="Trashmasters",
  database="smartbin"
)
mycursor = mydb.cursor()
#labelstring               #used as a field in the database


#Function to use the Google Vision API
#It performs the image processing and prints
#the associated labels for the image
def labeldetection(path):

    client = vision.ImageAnnotatorClient()
    file_name = path

    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    #Performs label detection
    response = client.label_detection(image=image)
    labels = response.label_annotations

    #prints out the labels the Vision API has identified from the image
    #labels is the actual data recieved from Google
    print('Labels:')
    global labelstring               #used as a field in the database
    labelstring = ""
    for label in labels:
        print(label.description)
        labelstring = labelstring + label.description + ", "


    #Array of items which are deemed to be recyclable
    #The returned labels will be checked against these to determine
    #if the object is recyclable or not
    Recyclablematerials = ["Plastic", "Bottle", "Plastic bottle",
                            "Paper", "Paper product", "Metal",
                            "Aluminum", "Aluminum can", "Tin can", "Beverage can"]
    detectedmaterial = "Trash"
    resultsent = False

    #Loops through labels to detect recyclable material
    for label in labels:
        for material in Recyclablematerials:
            if(label.description == material):
                print("")
                print("Recyclable material has been detected!: {0}" .format(label.description))
                sock.send(label.description)
                resultsent = True
                detectedmaterial = label.description
                break
        else:
            continue
        break

    #if no recyclable material was found then the default is trash
    if(resultsent == False):
        sock.send(detectedmaterial)

    return detectedmaterial


#Main Program Loop
try:
    while True:
        input_state = GPIO.input(18)
        if input_state == False:

            #Calls a subprocess of a shell executable responsible
            #for taking the image using fswebcam
            #Image is stored in the directory used to call the labeldetection function
            subprocess.call(['/home/pi/capture.sh'])
            print("Processing Image, Thank You")

            result = labeldetection('/home/pi/Pictures/image.jpg')

            #Inserts the labels from the Vision API and the decided result into the database
            mycursor.execute("INSERT INTO objects_thrown_away (Vision_API_Labels, Result) VALUES ('%s', '%s')" % (labelstring, result))
            mydb.commit()

except KeyboardInterrupt:
    GPIO.cleanup()
    sock.close()
    mydb.close()
