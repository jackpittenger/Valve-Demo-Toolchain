from helpers.read_int import read_int
from helpers.read_uchar import read_uchar

class RawData:

    def __init__(self, f):
        self.size = read_int(f)
        self.data = read_uchar(f, self.size)

