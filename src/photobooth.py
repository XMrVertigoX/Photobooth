import configparser, picamera, pygame, shutil, subprocess, time

# Local libraries
import button, display, pngview

config = configparser.ConfigParser()
config.read('photobooth.ini')

button.init()

display = display.Display(int(config['Display']['width']),
                          int(config['Display']['height']))

buttons = {
    'green': button.Button(int(config['Buttons']['green'])),
    'red': button.Button(int(config['Buttons']['red']))
}

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

captureName = 'capture.jpg'

previewCamera = picamera.PiCamera()
previewCamera.vflip = config['Misc']['previewFlip']


## ----- Functions -------------------------------------------------------------

def setupPygame():
    pygame.init()
    pygame.mouse.set_visible(0)
    display.gameScreen = pygame.display.set_mode((display.width, display.height))

def setupPreviewCamera():
    previewCamera = picamera.PiCamera()
    previewCamera.vflip = config['Misc']['previewFlip']

def takeAPicture():
    captureProcess = subprocess.Popen(['gphoto2', '--capture-image-and-download',
                                      '--force-overwrite', '--filename=' + captureName])
    captureProcess.wait()

def disablePreview():
    previewCamera.stop_preview()

def enablePreview():
    previewCamera.start_preview()

def savePhoto():
    safeTime = str(time.time())
    shutil.move(captureName, config['Paths']['photos'] + '/' 
                + config['Misc']['imagePrefix'] + safeTime + '.jpg')

def aspect_scale(img,(bx,by)):
    ix,iy = img.get_size()
    
    if ix > iy:
        # fit to width
        scale_factor = bx/float(ix)
        sy = scale_factor * iy
        
        if sy > by:
            scale_factor = by/float(iy)
            sx = scale_factor * ix
            sy = by
        
        else:
            sx = bx
    
    else:
        # fit to height
        scale_factor = by/float(iy)
        sx = scale_factor * ix
        
        if sx > bx:
            scale_factor = bx/float(ix)
            sx = bx
            sy = scale_factor * iy
        
        else:
            sy = by

    return pygame.transform.scale(img, (sx,sy))


## ----- Setup -----------------------------------------------------------------

setupPygame()
enablePreview()

pngImages['foto'].show()


## ----- Infinite loop ---------------------------------------------------------

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

        image = pygame.image.load(captureName)
        scaledImage = aspect_scale(image, (display.width, display.height))
        
        display.gameScreen.blit(scaledImage, (0, 0))

        display.gameScreen.blit(pygameImages['ok'], (0, 0))
        pygame.display.update()

        disablePreview()
        pngImages['wait'].terminate()

        while not buttons['green'].isPressed():
            pass

        #waitUntil(buttons['green'].isPressed())

        savePhoto()

        display.gameScreen.fill((0, 0, 0))
        pygame.display.update()

        enablePreview()

        pngImages['foto'].show()
