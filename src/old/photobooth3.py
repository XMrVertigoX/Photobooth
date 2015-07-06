#!/usr/bin/env python
#(c) Ben Fassbender

import pygame,sys, os, time, glob, shutil
import RPi.GPIO as GPIO
import pygame.camera
from pygame.locals import *

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(10, GPIO.IN)
GPIO.setup(9, GPIO.IN)

#misc-Variablen

width=640
height=480
t_last_photo= time.time()
t_cd = 5
flip_h = 0
flip_v = 1

dslr_usb=str(os.popen("lsusb -d 04b0:").readlines())[17:][:3] 	

#Pfade

dir_prg = "/home/pi/photobooth/"
dir_pics = "/media/usb/"

#Webcam

pygame.init()
pygame.camera.init()
pygame.mouse.set_visible(0)
pygame.font.init()
screen = pygame.display.set_mode((width,height))
cam = pygame.camera.Camera("/dev/video0",(width,height))
p_count=len(glob.glob(dir_pics+"Fotos/*"))

#Bildvariablen

img_cd1 = pygame.image.load(dir_prg + "1.png")
img_cd2 = pygame.image.load(dir_prg + "2.png")
img_cd3 = pygame.image.load(dir_prg + "3.png")
img_s = pygame.image.load(dir_prg + "smile.png")
img_w = pygame.image.load(dir_prg + "wait.png")
img_ok = pygame.image.load(dir_prg + "ok.png")
img_foto = pygame.image.load(dir_prg + "foto.png")


cam.start()
cam.set_controls(hflip = False, vflip = False)


os.system("sudo mount -t vfat -o uid=pi,gid=pi /dev/sda1 "+dir_pics)
os.system("sudo ./usbreset /dev/bus/usb/001/"+dslr_usb)

#if os.path.isfile(dir_prg + "/Foto/*"):
#	os.system("sudo rm "+ dir_prg +"Foto/*")


while 1:
	image = pygame.transform.flip(cam.get_image(),flip_v,flip_h)
	
	if (time.time()-t_last_photo) > 840 :
		os.system("irsend SEND_ONCE Nikon2 shutter")
		time.sleep(1)	
		os.system("sudo ./usbreset /dev/bus/usb/001/"+dslr_usb)
		os.system("gphoto2 -R -d=2")
		t_last_photo= time.time()
		
	screen.blit(image,(0,0))							#Live-Bild
	screen.blit(img_foto,(0,0))
	pygame.display.update()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			os.system("sudo umount "+dir_pics)
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				sys.exit()
	if GPIO.input(10) == 0 :
		dslr_usb=str(os.popen("lsusb -d 04b0:").readlines())[17:][:3]	 	#Device-ID der DSLR (Nur NIkon!)
		os.system("sudo ./usbreset /dev/bus/usb/001/"+dslr_usb)
		p_count=len(glob.glob(dir_pics+"Fotos/*")) + 1
		
		if p_count <1000:							#Ermittlung des letzten Fotos
			p_count_string = str(p_count)
		if p_count < 100:
			p_count_string = "0" + str(p_count)
		if p_count < 10:
			p_count_string = "00" + str(p_count)
		
		
		for i in range(0,t_cd):							#Countdown
			image = pygame.transform.flip(cam.get_image(),flip_v,flip_h)
			screen.blit(image,(0,0))
			screen.blit(img_cd3,(0,0))
			pygame.display.update()
		for i in range(0,t_cd):
			image = pygame.transform.flip(cam.get_image(),flip_v,flip_h)
			screen.blit(image,(0,0))
			screen.blit(img_cd2,(0,0))
			pygame.display.update()				
		for i in range(0,t_cd):			
			image = pygame.transform.flip(cam.get_image(),flip_v,flip_h)
			screen.blit(image,(0,0))
			screen.blit(img_cd1,(0,0))
			pygame.display.update()
		for i in range(0,4):
			image = pygame.transform.flip(cam.get_image(),flip_v,flip_h)
			screen.blit(image,(0,0))
			screen.blit(img_s,(0,0))
			pygame.display.update()
			
		os.system("irsend SEND_ONCE Nikon2 shutter")				#Kamera ausloesen
		time.sleep(1)
		screen.blit(image,(0,0))
		screen.blit(img_w,(0,0))
		pygame.display.update()

		os.system("gphoto2 --filename "+ dir_prg + "Foto/DSC_0001.JPG --force-overwrite -p 2")
		os.system("sudo ./usbreset /dev/bus/usb/001/"+dslr_usb)
		os.system("gphoto2 -R -d=2")
		if os.path.isfile(dir_prg + "/Foto/DSC_0001.JPG"):
			shutil.move(dir_prg + "/Foto/DSC_0001.JPG",dir_pics + "Fotos/DSC_0" + p_count_string +".JPG")
			if os.path.isfile(dir_prg + "/Foto/*"):
				os.system("sudo rm "+ dir_prg +"Foto/*")
			lastimage = pygame.image.load(dir_pics + "Fotos/DSC_0" + p_count_string +".JPG")
			lastimage_scale = pygame.transform.scale(lastimage, (640,425))
			pygame.display.update()

			screen.fill((0,0,0))
			while GPIO.input(9) == 1:
		 		screen.blit(pygame.transform.flip(lastimage_scale,flip_v,flip_h),(0,0))
				screen.blit(pygame.font.Font(None,30).render(p_count_string,0,(255,255,255)),(0,0))
				screen.blit(img_ok,(0,0))
				pygame.display.update()
