import logging
import sys

from multiprocessing import Process
from subprocess import run
# import tkinter

from picamera import PiCamera
# from PIL import Image
# from watchdog.observers import Observer
# from watchdog.events import PatternMatchingEventHandler

# from display import Display
# from file import File
# from util import aspectScale
# from pngview import PNGView


class Photobooth():
    filename = 'capture.jpg'

    def __init__(self, config):
        self.__config = config
        self.__setupPreviewCamera()

    def __setupPreviewCamera(self):
        logging.debug("setupPreviewCamera")
        self.__previewCamera = PiCamera()
        self.__previewCamera.vflip = self.__config['preview']['vflip']

    def stopPreview(self):
        logging.debug("stopPreview")
        self.__previewCamera.stop_preview()

    def startPreview(self):
        logging.debug("startPreview")
        self.__previewCamera.start_preview()

    def capturePhoto(self):
        logging.debug("capturePhoto")
        run(['gphoto2', '--capture-image-and-download', '--force-overwrite',
             '--filename={0}'.format(filename)])
