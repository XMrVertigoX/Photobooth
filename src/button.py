import RPi.GPIO as GPIO

isInit = False

def init(mode = GPIO.BCM):
	GPIO.setmode(mode)

	global isInit
	isInit = True

class Button:
	def __init__(self, gpio, direction = GPIO.IN, pull_up_down = GPIO.PUD_DOWN):
		self.gpio = gpio
		self.direction = direction

		GPIO.setup(self.gpio, self.direction, pull_up_down)

	def isPressed(self):
		return GPIO.input(self.gpio)

if __name__ == '__main__':
	pass
