import RPi.GPIO as GPIO

def init(mode = GPIO.BCM):
	GPIO.setmode(mode)

def cleanup():
	GPIO.cleanup()

class Button:
	def __init__(self, gpio, direction = GPIO.IN):
		self.__gpio = gpio
		self.__direction = direction
		GPIO.setup(self.__gpio, self.__direction)

	def isPressed(self):
		return not GPIO.input(self.__gpio)
