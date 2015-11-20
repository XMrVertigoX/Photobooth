import pygame, shutil, time, os

from picamera import PiCamera
from configparser import ConfigParser
from subprocess import Popen
from multiprocessing import Process
from PIL import Image

# Local modules
import button

from display import Display
from file import File
from util import aspectScale
from pngview import PNGView


## ----- Functions -------------------------------------------------------------

def setupPygame():
    pygame.init()
    pygame.mouse.set_visible(0)
    display.gameScreen = pygame.display.set_mode(display.getSize())

def setupPreviewCamera():
    previewCamera = picamera.PiCamera()
    previewCamera.vflip = config['Misc']['previewFlip']

def savePhoto():
    safeTime = str(time.time())

    tempLocation = '/tmp/'
    tempFile = tempLocation + safeTime + captureFormat

    shutil.move(captureName + captureFormat, tempFile)

    backupDirectory = config['Paths']['backup'] + '/'
    photosDirectory = config['Paths']['photos'] + '/'

    if not os.path.exists(config['Paths']['backup']):
        os.mkdir(config['Paths']['backup'])

    fileName = imagePrefix + safeTime + captureFormat

    shutil.copy(tempFile, photosDirectory + fileName)
    shutil.copy(tempFile, backupDirectory + fileName)

    if config['Misc']['logo']:
        tempFileWithLogo = tempLocation + safeTime + logoSuffix + captureFormat
        fileNameWithLogo = imagePrefix + safeTime + logoSuffix + captureFormat

        logo = Image.open('images/logo.png')
        logo = logo.convert('RGBA')

        photo = Image.open(tempFile)
        photo = photo.convert('RGBA')

        compositeImage = Image.alpha_composite(photo, logo)
        compositeImage.save(tempFileWithLogo)

        shutil.copy(tempFileWithLogo, photosDirectory + fileNameWithLogo)
        shutil.copy(tempFileWithLogo, backupDirectory + fileNameWithLogo)

        os.remove(tempFileWithLogo)

    os.remove(tempFile)


## ----- Setup -----------------------------------------------------------------

config = ConfigParser()
config.read('photobooth.ini')

button.init()

buttons = {
    'green': button.Button(int(config['Buttons']['green'])),
    'red': button.Button(int(config['Buttons']['red']))
}

display = Display(int(config['Display']['width']), int(config['Display']['height']))

pngImages = {
    'foto': PNGView('images/foto.png'),
    'smile': PNGView('images/smile.png'),
    'timer_1': PNGView('images/timer_1.png'),
    'timer_2': PNGView('images/timer_2.png'),
    'timer_3': PNGView('images/timer_3.png'),
    'wait': PNGView('images/wait.png')
}

pygameImages = {
    'ok': pygame.image.load('images/ok.png')
}

sleep = float(config['Misc']['countdownSleep'])

flags = {
    'capture': False,
    'run': True
}

captureName = config['Misc']['captureName']
captureFormat = '.' + config['Misc']['captureFormat']

imagePrefix = config['Misc']['imagePrefix']
logoSuffix = config['Misc']['logoSuffix']

previewCamera = PiCamera()
previewCamera.vflip = config['Misc']['previewFlip']
previewCamera.zoom = (0.1, 0.1, 0.8, 0.8)

setupPygame()

enablePreview()

pngImages['foto'].show()


# ----- Infinite loop ----------------------------------------------------------

while flags['run']:
    #flags['run'] = False

    if buttons['red'].isPressed():
        flags['capture'] = True
        pngImages['foto'].terminate()

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

        pngImages['smile'].show()

        takeAPicture()

        pngImages['smile'].terminate()

        pngImages['wait'].show()

        if os.path.exists(captureName + '.jpg'):
            image = pygame.image.load(captureName + '.jpg')
            scaledImage = aspectScale(image, display.getSize())

            display.gameScreen.blit(scaledImage, (0, 0))

            display.gameScreen.blit(pygameImages['ok'], (0, 0))

            disablePreview()

            pngImages['wait'].terminate()

            pygame.display.update()

            # Wait for green button
            while not buttons['green'].isPressed():
                pass

            saveProcess = Process(target=savePhoto)
            saveProcess.start()

        else:
            if os.path.exists(captureName + '.jpg'):
                os.remove(captureName + '.jpg')

            if os.path.exists(captureName + '_logo.jpg'):
                os.remove(captureName + '_logo.jpg')

            pngImages['wait'].kill()

        display.gameScreen.fill((0, 0, 0))
        pygame.display.update()

        enablePreview()

        pngImages['foto'].show()


# ----- Quit program -----------------------------------------------------------

for image in pngImages:
    image.kill()

previewCamera.close()

button.cleanup()
