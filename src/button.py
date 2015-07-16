import RPi.GPIO as GPIO

isInit = False

def init(mode = GPIO.BCM):
	GPIO.setmode(mode)

	global isInit
	isInit = True

class Button:
	def __init__(self, gpio, direction = GPIO.IN):
		self.gpio = gpio
		self.direction = direction

		GPIO.setup(self.gpio, self.direction)

	def isPressed(self):
		return not GPIO.input(self.gpio)

if __name__ == '__main__':
	pass
