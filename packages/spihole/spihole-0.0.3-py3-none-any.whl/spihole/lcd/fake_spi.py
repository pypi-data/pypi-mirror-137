class SpiDev(object):
    def __init__(self, bus, device):
        self.bus = bus
        self.device = device
        self.max_speed_hz = 0
        self.mode = 0

    def writebytes(self, data):
        pass
