import subprocess

class PNGView():
	binary = 'pngview/pngview'
	running = False

	def __init__(self, path, layer = 3):
		self.path = path
		self.layer = layer
		
	def show(self):
		self.process = subprocess.Popen(binary, "-l" + str(self.layer), str(self.path)])
		
		global running
		running = True

	def terminate(self):
		if running:
			self.terminate()

	def setPath(self, path):
		self.path = path

	def setLayer(self, layer):
		self.layer = layer

if __name__ == '__main__':
	pass
