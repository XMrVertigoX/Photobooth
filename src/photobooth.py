#! /bin/python2

import configparser
import picamera
import pygame
import RPi.GPIO as GPIO
import shutil
import subprocess
import time, datetime

import pngview

config = configparser.ConfigParser()
config.read('photobooth.ini')

pygame.init()
pygame.mouse.set_visible(0)

screen = pygame.display.set_mode((1920, 1080))

previewCamera = picamera.PiCamera()
previewCamera.vflip = config['Misc']['previewFlip']

flags = {
	'run': True,
	'capture': False
}

global fotoButton

## ----- Functions -------------------------------------------------------------

def setupGPIO():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(9, GPIO.IN)
	GPIO.setup(10, GPIO.IN)

def takeAPicture():
	captureProcess = subprocess.Popen(['gphoto2', '--capture-image-and-download'])
	captureProcess.wait()

def disablePreview():
	previewCamera.stop_preview()

def enablePreview():
	previewCamera.start_preview()

def archivePicture():
	safeTime = str(time.time())
	shutil.move('capt0000.jpg', config['Paths']['output'] + '/' + config['Misc']['imagePrefix'] + safeTime + '.jpg')

## ----- Setup -----------------------------------------------------------------

setupGPIO();
enablePreview();

## ----- Infinite loop ---------------------------------------------------------

fotoButton = pngview.show("images/foto.png", 3)

while flags['run']:
	#flags['run'] = False

	if not GPIO.input(10):
		flags['capture'] = True
		fotoButton.terminate()

	if flags['capture']:
		flags['capture'] = False

		p = pngview.show("images/timer_3.png", 3)
		time.sleep(1.5)
		p.terminate()

		p = pngview.show("images/timer_2.png", 3)
		time.sleep(1.5)
		p.terminate()

		p = pngview.show("images/timer_1.png", 3)
		time.sleep(1.5)
		p.terminate()

		p = pngview.show("images/smile.png", 3)
		
		takeAPicture()

		#captureProcess = subprocess.Popen(['gphoto2', '--capture-image-and-download', '--filename=' + config['Paths']['output'] + '/' + str(time.time()) + '.jpg'])
		#captureProcess = subprocess.Popen(['gphoto2', '--capture-image-and-download'])
		#captureProcess.wait()

		p.terminate()

		p = pngview.show("images/wait.png", 3)

		image = pygame.image.load("capt0000.jpg")
		scaledImage = pygame.transform.scale(image, (1280, 1024))
		screen.blit(scaledImage, (0, 0))

		button = pygame.image.load("images/ok.png")
		screen.blit(button, (0, 0))

		disablePreview()

		pygame.display.update()

		p.terminate()

		while GPIO.input(9):
			pass

		archivePicture()

		screen.fill((0, 0, 0))
		pygame.display.update()

		enablePreview()

		fotoButton = pngview.show("images/foto.png", 3)

## ----- End program -----------------------------------------------------------

previewCamera.close()
