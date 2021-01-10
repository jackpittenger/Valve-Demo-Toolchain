import struct

from helpers.read_bool import read_bool
from helpers.read_string import read_string
from helpers.read_char import read_char
from helpers.read_short import read_short
from helpers.read_int import read_int


class Dem_Stringtables:
    #https://theportalwiki.com/wiki/User:WindPower/DemParser.py
    def __init__(self, f):
        self.length = read_int(f)
        self.raw = f.read(self.length) 
