import configparser, subprocess

config = configparser.ConfigParser()
config.read('photobooth.ini')

bin = config['Paths']['bin']

def show(image, layer):
	return subprocess.Popen([config['Paths']['bin'] + "/pngview", "-l" + str(layer), image])
