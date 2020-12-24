from helpers.read_float import read_float

class Vector:
    
    def __init__(self, f):
        self.x = read_float(f)
        self.y = read_float(f)
        self.z = read_float(f)

