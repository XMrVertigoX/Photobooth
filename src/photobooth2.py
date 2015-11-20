import logging, time
from multiprocessing import Process
from subprocess import Popen
# import tkinter

# Additional modules
from picamera import PiCamera
from configparser import ConfigParser
# from PIL import Image
# from watchdog.observers import Observer
# from watchdog.events import PatternMatchingEventHandler

# Local modules
# import button
# from display import Display
# from file import File
# from util import aspectScale
# from pngview import PNGView

class Photobooth():
    def __init__(self, config):
        logging.debug("__init__")

    def setupPreviewCamera(self):
        logging.debug("setupPreviewCamera")
        self.__previewCamera = PiCamera()
        self.__previewCamera.vflip = self.__config['preview']['vflip']

    def stopPreview(self):
        logging.debug("stopPreview")
        if self.__previewCamera:
            self.__previewCamera.stop_preview()
        else:
            logging.warning("No preview camera set!")

    def startPreview(self):
        logging.debug("startPreview")
        if self.__previewCamera:
            self.__previewCamera.start_preview()
        else:
            logging.warning("No preview camera set!")

    def capturePhoto(self):
        logging.debug("capturePhoto")
        run(['gphoto2', '--capture-image-and-download', '--force-overwrite',
                '--filename={0}.jpg'.format(self.__config['capture']['fileName'])])

    def savePhoto(self):
        pass

def main():
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    logging.debug("Entering main routine")
    config = ConfigParser().read('photobooth.ini')
    # config.read(configFile) TODO
    photobooth = Photobooth(config)
    setupPreviewCamera()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for image in pngImages:
            image.kill()
        previewCamera.close()
        button.cleanup()

if __name__ == '__main__':
    main()
