#!/usr/bin/env python

import pygame,sys, os, time
import RPi.GPIO as GPIO
import pygame.camera
from pygame.locals import *

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(10, GPIO.IN)
GPIO.setup(9, GPIO.IN)

pygame.init()
pygame.camera.init()
pygame.mouse.set_visible(0)
screen = pygame.display.set_mode((640,480))

cam = pygame.camera.Camera("/dev/video1",(640,480))
cam.start()
cam.set_controls(hflip = True, vflip = False)

cd1 = pygame.image.load("/home/pi/Desktop/photobooth/1.png")
cd2 = pygame.image.load("/home/pi/Desktop/photobooth/2.png")
cd3 = pygame.image.load("/home/pi/Desktop/photobooth/3.png")
cds = pygame.image.load("/home/pi/Desktop/photobooth/smile.png")
cdw = pygame.image.load("/home/pi/Desktop/photobooth/wait.png")
cdok = pygame.image.load("/home/pi/Desktop/photobooth/ok.png")

p_count = len([name for name in os.listdir('.') if os.path.isfile(name)])-8

while 1:
	image = pygame.transform.flip(cam.get_image(),1,0)
	screen.blit(image,(0,0))
	screen.blit(cdok,(0,0))
	pygame.display.update()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				sys.exit()
	if GPIO.input(10) == 0 :
		os.system("sudo ./usbreset /dev/bus/usb/001/014")
		p_count = p_count + 1
		if p_count <1000:
			p_count_string = str(p_count)
		if p_count < 100:
			p_count_string = "0" + str(p_count)
		if p_count < 10:
			p_count_String = "00" + str(p_count)
		
		#os.rename("capt0000.jpg",p_counts)
		for i in range(0,10):
			image = pygame.transform.flip(cam.get_image(),1,0)
			screen.blit(image,(0,0))
			screen.blit(cd3,(0,0))
			pygame.display.update()
			#pygame.time.wait(3)
		screen.blit(image,(0,0))
		for i in range(0,10):
			image = pygame.transform.flip(cam.get_image(),1,0)
			screen.blit(image,(0,0))
			screen.blit(cd2,(0,0))
			pygame.display.update()
			#pygame.time.wait(3)
			screen.blit(image,(0,0))			
		#os.system("gphoto2 --capture-image-and-download &")	
		screen.blit(image,(0,0))		
		for i in range(0,10):			
			image = pygame.transform.flip(cam.get_image(),1,0)
			screen.blit(image,(0,0))
			screen.blit(cd1,(0,0))
			pygame.display.update()
			#pygame.time.wait(3)
		screen.blit(image,(0,0))
		image = pygame.transform.flip(cam.get_image(),1,0)
		screen.blit(image,(0,0))
		screen.blit(cds,(0,0))
		pygame.display.update()
			#pygame.time.wait(3)			
		os.system("gphoto2 --capture-image-and-download")
		screen.blit(image,(0,0))
		screen.blit(cdw,(0,0))
		pygame.display.update()
		#time.sleep(3)
		lastimage = pygame.image.load("DSC_0" + p_count_string +".JPG")
		#foto = pygame.image.load("capt0000.jpg")
		lastimage_scale = pygame.transform.scale(lastimage, (640,425))
		#pygame.screen.fill(0,0,0)
		while GPIO.input(9) == 1:
			screen.blit(lastimage_scale,(0,0))
			screen.blit(cdok,(0,0))
			pygame.display.update()
	
	
