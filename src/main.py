import logging
import sys
from argparse import ArgumentParser
from configparser import ConfigParser

import buttons
from buttons import Button
from photobooth2 import Photobooth


def parseArguments():
    parser = ArgumentParser()
    parser.add_argument('-c', '--config', default='photobooth.ini')
    return vars(parser.parse_args())


def setup():
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)


def main():
    arguments = parseArguments()
    config = ConfigParser()
    config.read(arguments['config'])
    photobooth = Photobooth(config)
    photobooth.startPreview()
    buttons.init()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        photobooth.stopPreview()
        buttons.cleanup()
        sys.exit()

if __name__ == '__main__':
    main()
