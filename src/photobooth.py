import pygame, shutil, time

from picamera import PiCamera
from configparser import ConfigParser
from subprocess import Popen
from multiprocessing import Process
from PIL import Image

# Local libraries
import button, display, pngview
from util import aspectScale


## ----- Functions -------------------------------------------------------------

def setupPygame():
    pygame.init()
    pygame.mouse.set_visible(0)
    display.gameScreen = pygame.display.set_mode(display.getSize())

def setupPreviewCamera():
    previewCamera = picamera.PiCamera()
    previewCamera.vflip = config['Misc']['previewFlip']

def takeAPicture():
    captureProcess = Popen(['gphoto2',
                            '--capture-image-and-download',
                            '--force-overwrite',
                            '--filename=' + captureName +'.jpg'])

    captureProcess.wait()

def disablePreview():
    previewCamera.stop_preview()

def enablePreview():
    previewCamera.start_preview()

def savePhoto():
    safeTime = str(time.time())

    if config['Misc']['logo']:
        logo = Image.open("images/logo.png")
        logo = logo.convert("RGBA")

        photo = Image.open(captureName + '.jpg')
        photo = photo.convert('RGBA')

        compositeImage = Image.alpha_composite(photo, logo)
        compositeImage.save(captureName + '_logo.jpg')

        shutil.copy(captureName + "_logo.jpg", config['Paths']['photos'] + '/' 
                    + config['Misc']['imagePrefix'] + safeTime + '_logo.jpg')
        shutil.move(captureName + "_logo.jpg", config['Paths']['backup'] + '/' 
                    + config['Misc']['imagePrefix'] + safeTime + '_logo.jpg')

    shutil.copy(captureName + ".jpg", config['Paths']['photos'] + '/' 
                + config['Misc']['imagePrefix'] + safeTime + '.jpg')
    shutil.move(captureName + ".jpg", config['Paths']['backup'] + '/' 
                + config['Misc']['imagePrefix'] + safeTime + '.jpg')


## ----- Setup -----------------------------------------------------------------

config = ConfigParser()
config.read('photobooth.ini')

button.init()

buttons = {
    'green': button.Button(int(config['Buttons']['green'])),
    'red': button.Button(int(config['Buttons']['red']))
}

display = display.Display(int(config['Display']['width']),
                          int(config['Display']['height']))

pngImages = {
    'foto': pngview.PNGView('images/foto.png'),
    'smile': pngview.PNGView('images/smile.png'),
    'timer_1': pngview.PNGView('images/timer_1.png'),
    'timer_2': pngview.PNGView('images/timer_2.png'),
    'timer_3': pngview.PNGView('images/timer_3.png'),
    'wait': pngview.PNGView('images/wait.png')
}

pygameImages = {
    'ok': pygame.image.load('images/ok.png')
}

sleep = float(config['Misc']['countdownSleep'])

flags = {
    'run': True,
    'capture': False
}

captureName = config['Misc']['captureName']

previewCamera = picamera.PiCamera()
previewCamera.vflip = config['Misc']['previewFlip']

setupPygame()


# ----- Prepare ----------------------------------------------------------------

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

        image = pygame.image.load(captureName + '.jpg')
        scaledImage = aspectScale(image, display.getSize())
        
        display.gameScreen.blit(scaledImage, (0, 0))

        display.gameScreen.blit(pygameImages['ok'], (0, 0))
        pygame.display.update()

        disablePreview()

        pngImages['wait'].terminate()

        # Wait for green button
        while not buttons['green'].isPressed():
            pass

        saveProcess = Process(target=savePhoto)
        saveProcess.start()

        display.gameScreen.fill((0, 0, 0))
        pygame.display.update()

        enablePreview()

        pngImages['foto'].show()


# ----- Quit program -----------------------------------------------------------

disablePreview()
pngImages['foto'].terminate()
