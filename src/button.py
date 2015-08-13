import RPi.GPIO as GPIO

def init(mode = GPIO.BCM):
	GPIO.setmode(mode)

def cleanup():
	GPIO.cleanup()

class Button:
	def __init__(self, gpio, direction = GPIO.IN):
		self.gpio = gpio
		self.direction = direction

		GPIO.setup(self.gpio, self.direction)

	def isPressed(self):
		return not GPIO.input(self.gpio)
