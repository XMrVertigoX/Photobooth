import logging, shutil
from multiprocessing import Process
from subprocess import run
# TODO import tkinter

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
    def __init__(self, configFile):
        logging.debug("__init__")
        self.__config = ConfigParser()
        self.__config.read(configFile)
        __setupPreviewCamera()

    def __setupPreviewCamera(self):
        logging.debug("__setupPreviewCamera")
        self.__previewCamera = PiCamera()
        self.__previewCamera.vflip = self.__config['preview']['vflip']

    def stopPreview(self):
        self.__previewCamera.stop_preview()

    def startPreview(self):
        self.__previewCamera.start_preview()

    def capturePhoto(self):
        logging.debug("capture")
        run(['gphoto2', '--capture-image-and-download', '--force-overwrite',
                '--filename={0}.jpg'.format(self.__config['capture']['fileName'])])

def main():
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    logging.debug("Entering main function")
    photobooth = Photobooth('photobooth2.ini')

if __name__ == '__main__':
    main()
