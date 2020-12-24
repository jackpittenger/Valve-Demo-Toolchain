from helpers.read_int import read_int

from structures.Democmdinfo_t import Democmdinfo_t
from structures.RawData import RawData

class Dem_Signon:
    
    def __init__(self, f):
        self.demo_cmd_info = Democmdinfo_t(f)
        self.sin = read_int(f)
        self.sout = read_int(f)
        self.netpackets = RawData(f)
