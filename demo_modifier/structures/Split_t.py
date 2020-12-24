from helpers.read_float import read_float
from helpers.read_int import read_int

from structures.QAngle import QAngle
from structures.Vector import Vector

class Split_t:
    
    def __init__(self, f):
        self.flags = read_int(f)
        self.view_origin = Vector(f)
        self.view_angles = QAngle(f)
        self.local_view_angles = QAngle(f)
        self.view_origin_2 = Vector(f)
        self.view_angles_2 = QAngle(f)
        self.local_view_angles_2 = QAngle(f)

