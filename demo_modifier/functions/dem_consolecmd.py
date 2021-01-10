import struct

from helpers.read_int import read_int
from helpers.read_string import read_string

class Dem_Consolecmd:

    def __init__(self, f):
        self.length = read_int(f)
        self.cmd = read_string(f, self.length)
        print("CMD: "+str(self.cmd))
