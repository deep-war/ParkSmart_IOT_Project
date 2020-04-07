#***************************************************************************
# This file reads the status of magnetic sensor and outputs the parking 
# availibility status of each parking spot as json. Also if car comes in reserved parking spot 
# camera takes picture of car number plate and then outputs detected number plate 
# in json  
# Author: Group1 - Deepthi Warrier, Tejashri Joshi
# Date: 16-March-2020
#*************************************************************************
import json
import time
from grovepi import *
import sys
from picamera import PiCamera
import time
import cv2
import imutils
import numpy as np
import pytesseract

# Import flask libraries
from flask import Flask, render_template

# import the GrovePi+ libraries
from grovepi import *


# initialize sensor digital port for Parking Spots
magnetic_sensor_ps1 = 6 # digital port 6 will be used for parking spot 1 sensor
greenled_ps1 = 5 #digital port 5 for led for parking spot1

magnetic_sensor_ps2 = 8 # digital port 8 will be used for parking spot 2 sensor
greenled_ps2 = 7 #digital port 7 for led for parking spot2

magnetic_sensor_ps3 = 2 # digital port 2 will be used for parking spot 3 sensor
redled_ps3 = 3  #digital port 3 for led for parking spot3

# Set the digital port 6,8,2 pinMode to input
pinMode(magnetic_sensor_ps1,"INPUT")
pinMode(magnetic_sensor_ps2,"INPUT")
pinMode(magnetic_sensor_ps3,"INPUT")
# Set the digital port 5,7,3 pinMode to output
pinMode(greenled_ps1,"OUTPUT")
pinMode(greenled_ps2,"OUTPUT")
pinMode(redled_ps3,"OUTPUT")

def getData(name):
    ps3_number_plate = ''
    try:
            #reads the magnetic sensor 1 value and sets value for parking 1 status
            magnet_output_ps1 = digitalRead(magnetic_sensor_ps1)
            if(magnet_output_ps1 == 1):
                digitalWrite(greenled_ps1,0)
                parking_available_ps1 = "Occupied"
                
            else:
                digitalWrite(greenled_ps1,1)
                parking_available_ps1 = "Available"
                
                
            #reads the magnetic sensor 2 value and sets value for parking 2 status
            magnet_output_ps2 = digitalRead(magnetic_sensor_ps2)
            if(magnet_output_ps2 == 1):
                digitalWrite(greenled_ps2,0)
                parking_available_ps2 = "Occupied"
                
            else:
                digitalWrite(greenled_ps2,1)
                parking_available_ps2 = "Available"
                
                
            #reads the magnetic sensor 3 value and sets value for parking 3 status
            magnet_output_ps3 = digitalRead(magnetic_sensor_ps3)
            
            redled_output_ps3 = digitalRead(redled_ps3)
            
            if(magnet_output_ps3 == 1 or redled_output_ps3 == 1):
                digitalWrite(redled_ps3,1)
                parking_available_ps3 = "Occupied"

            else:
                #digitalWrite(redled_ps3,1)
                parking_available_ps3 = "Available"


            # if the car is in reserved parking spot take a picture of numberplate and detect plate
            if(magnet_output_ps3 == 1):
                path = '/home/pi/Desktop/TCSS573_Class_Activities_GR01/Project/ps3.jpg'
                ps3_number_plate = detect_number_plate(path)                
                         
                                
            ## The redled needs to be set from the db                
            time.sleep(1)           
            # json having details of parking spot status and number plate
            data = {
                'name' : name,
                'ps3_number_plate':ps3_number_plate,
                'parkspot_ps1':1,
                'parkspot1status':parking_available_ps1,
                'parkspot_ps2':2,
                'parkspot2status':parking_available_ps2,
                'parkspot_ps3':3,
                'parkspot3status':parking_available_ps3               
            }
            #client.publish(topic,json.dumps(data))
            sys.stdout.write(json.dumps(data))
            sys.stdout.flush()
            sys.exit(0)
    except Exception as ex:
        digitalWrite(greenled_ps1, 0)
        digitalWrite(greenled_ps2, 0)
        digitalWrite(redled_ps3, 0)
        print('An error has occurred: %s' % ex)
    

# function to take a picture with camera
def get_image(image_path):
	camera = PiCamera()
	camera.rotation = 0

	time.sleep(5)
	camera.capture(image_path)


# function to detect the number plate from picture taken from camera
def detect_number_plate(image_path):

	get_image(image_path)

	img = cv2.imread(image_path, cv2.IMREAD_COLOR)

	img = cv2.resize(img, (620, 480))

	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert to grey scale
	gray = cv2.bilateralFilter(gray, 11, 17, 17)  # Blur to reduce noise
	edged = cv2.Canny(gray, 30, 200)  # Perform Edge detection

	# find contours in the edged image, keep only the largest
	# ones, and initialize our screen contour
	cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
	screenCnt = None

	# loop over our contours
	for c in cnts:
		# approximate the contour
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.018 * peri, True)

		# if our approximated contour has four points, then
		# we can assume that we have found our screen
		if len(approx) == 4:
			screenCnt = approx
			break

	if screenCnt is None:
		detected = 0
		
	else:
		detected = 1

	if detected == 1:
		cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)

		# Masking the part other than the number plate
		mask = np.zeros(gray.shape, np.uint8)
		new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1, )
		new_image = cv2.bitwise_and(img, img, mask=mask)

		# Now crop
		(x, y) = np.where(mask == 255)
		(topx, topy) = (np.min(x), np.min(y))
		(bottomx, bottomy) = (np.max(x), np.max(y))
		Cropped = gray[topx:bottomx + 1, topy:bottomy + 1]

		# Read the number plate
		text = pytesseract.image_to_string(Cropped, config='-l eng --oem 3 --psm 12')
		#print("Detected Number is:", text)
	else:
		text=""
	return text
    
if __name__ == '__main__':    
    try: 
        #while True:          
        getData('deepti')            
    except KeyboardInterrupt:
        digitalWrite(greenled_ps1, 0)
        digitalWrite(greenled_ps2, 0)
        digitalWrite(redled_ps3, 0)
        print("Exiting")
    except IOError:
        digitalWrite(greenled_ps1, 0)
        digitalWrite(greenled_ps2, 0)
        digitalWrite(redled_ps3, 0)
        print("IOError Occured")
    except Exception as ex:
        digitalWrite(greenled_ps1, 0)
        digitalWrite(greenled_ps2, 0)
        digitalWrite(redled_ps3, 0)
        print('An error has occurred: %s' % ex)
