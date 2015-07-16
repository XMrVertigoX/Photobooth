import configparser, picamera, pygame, shutil, subprocess, time, os

# Local libraries
import Button
from pngview import PNGView
from aspect_scale import aspect_scale

global display, previewCamera

config = configparser.ConfigParser()
config.read('photobooth.ini')

button.init()

buttons = {
	'green': button.Button(config['Buttons']['green']),
	'red': button.Button(config['Buttons']['red'])
}

pngImages = {
	'foto': PNGView('images/foto.png)',
	'smile': PNGView('images/smile.png'),
	'timer_1': PNGView('images/timer_1.png'),
	'timer_2': PNGView('images/timer_2.png'),
	'timer_3': PNGView('images/timer_3.png'),
	'wait': PNGView('images/wait.png)'
}

pygameImages = {
	'ok': pygame.image.load("images/ok.png")
}

screenWidth = config['Display']['width']
screenHeight = config['Display']['height']

sleep = config['Misc']['countdownSleep']

flags = {
	'run': True,
	'capture': False
}

captureName = 'capture.jpg'


## ----- Functions -------------------------------------------------------------

def setupPygame():
	pygame.init()
	pygame.mouse.set_visible(0)
	display = pygame.display.set_mode((screenWidth, screenHeight))

def setupPreviewCamera():
	previewCamera = picamera.PiCamera()
	previewCamera.vflip = config['Misc']['previewFlip']

def takeAPicture():
	captureProcess = subprocess.Popen(['gphoto2', '--capture-image-and-download', 'filename=' + captureName])
	captureProcess.wait()

def disablePreview():
	previewCamera.stop_preview()

def enablePreview():
	previewCamera.start_preview()

def savePhoto():
	safeTime = str(time.time())
	shutil.move(captureName, config['Paths']['output'] + '/' + config['Misc']['imagePrefix'] + safeTime + '.jpg')

def waitUntil(condition):
	while not condition:
		pass

def buttonPressed(gpio):
	pass

## ----- Setup -----------------------------------------------------------------

setupPygame()
setupPreviewCamera()

enablePreview()

pngImages['foto'].show()


## ----- Infinite loop ---------------------------------------------------------

while flags['run']:
	#flags['run'] = False

	if not GPIO.input(10):
		flags['capture'] = True
		fotoButton.terminate()

	if flags['capture']:
		flags['capture'] = False

		pngImages['timer_3'].show()
		time.sleep(sleep)
		pngImages['timer_3'].terminate()

		pngImages['timer_2'].show()
		time.sleep(sleep)
		pngImages['timer_2'].terminate()

		pngImages['timer_1'].show()
		time.sleep(sleep)
		pngImages['timer_1'].terminate()

		pngImages['smiles'].show()
		
		takeAPicture()

		pngImages['smiles'].terminate()

		pngImages['wait'].show()

		image = pygame.image.load("capt0000.jpg")
		scaledImage = pygame.transform.aspect_scale(image, (screenHeight, screenHeight))
		screen.blit(scaledImage, (0, 0))

		screen.blit(pygameImages['ok'], (0, 0))
		pygame.display.update()

		disablePreview()
		pngImages['wait'].terminate()

		waitUntil(not GPIO.input(9))

		savePhoto()

		screen.fill((0, 0, 0))
		pygame.display.update()

		enablePreview()

		fotoButton = pngview.show("images/foto.png")
