from helpers.read_float import read_float

class QAngle:
    
    def __init__(self, f):
        self.pitch = read_float(f)
        self.yaw = read_float(f)
        self.roll = read_float(f)

