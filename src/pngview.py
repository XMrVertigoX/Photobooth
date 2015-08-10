from subprocess import Popen

class PNGView():
    binary = 'pngview/pngview'
    running = False

    def __init__(self, path, layer = 3):
        self.path = path
        self.layer = layer
        
    def show(self):
        self.process = Popen([self.binary, "-l" + str(self.layer),
                                        self.path])
        self.running = True

    def terminate(self):
        if self.running:
            self.process.terminate()
