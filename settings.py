import os

class Run:
    def __init__(self):
        self.debug = True
        self.host = '0.0.0.0'
        
    def getPort(self, portENV='PORT', defPort=5000):
        try:
            if os.environ.get(portENV):
                if len(os.environ[portENV]) != 4:
                    raise Exception()
                return int(os.environ[portENV])
        
        except:
            return defPort