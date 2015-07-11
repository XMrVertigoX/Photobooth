#! /bin/python

import configparser, picamera, subprocess, RPi.GPIO as GPIO, time

config = configparser.ConfigParser()
config.read('photobooth.ini')

imgDir = config['paths']['imageDirectory']

run = False

lastPhoto = None

camera = picamera.PiCamera()

#dslr_usb=str(os.popen("lsusb -d 04b0:").readlines())[17:][:3]

## ----- Functions -------------------------------------------------------------

def countdown(seconds):
	for x in range(seconds):
		p = pngview(imgDir + "/" + (x+1) + ".png")
		time.sleep(1)
		p.terminate()

def capture():
	pass

def disablePreview():
	camera.stopPreview()

def enablePreview():
	camera.start_preview()

def pngview(imagePath):
	p = subprocess.Popen(["./bin/pngview", "-l 3", imagePath])
	return p

def makeAPicture():
	countdown(3)
	capture()

def setupGPIO():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(9, GPIO.IN)
	GPIO.setup(10, GPIO.IN)

## ----- Setup -----------------------------------------------------------------

setupGPIO();
enablePreview();

## ----- Infinite loop ---------------------------------------------------------

while 1:
	## Set the run flag if button is pressed
	if not GPIO.input(9):
		if not run:
			run = True

	
	if run:
		makeAPicture()
		run = False
