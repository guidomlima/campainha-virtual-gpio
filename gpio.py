class Gpio():
    def __init__(self,_id,pin,status):
        self._id = _id
        self.pin = pin
        self.status = status

    def setPin(self,pin):
        self.pin = pin

    def setStatus(self, status):
        self.status=status

    def getPin(self):
        return self.pin

    def getStatus(self):
        return self.status