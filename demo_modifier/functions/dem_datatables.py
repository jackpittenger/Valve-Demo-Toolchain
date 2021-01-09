from helpers.read_int import read_int
from helpers.read_char import read_char

class Dem_Datatables:
    
    def __init__(self, f):
        self.sin = read_int(f)
        for _ in range(0, self.sin):
            read_char(f)
