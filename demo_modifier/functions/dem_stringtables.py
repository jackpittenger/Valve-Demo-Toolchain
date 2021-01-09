import struct

from helpers.read_bool import read_bool
from helpers.read_string import read_string
from helpers.read_char import read_uchar
from helpers.read_short import read_short
from helpers.read_int import read_uint

class Dem_Stringtables:

    def __init__(self, f):
        self.is_file_names = read_bool(f) 
        self.table_name = read_string(f, 256)
        #for _ in range(0, 64):
        #    self.table_name += chr(struct.unpack("B", f.read(1))[0])
        self.max_entries = read_short(f)
        self.num_entries = read_short(f)
        self.data_length_in_bits = read_uint(f)
        self.is_user_data_fixed_size = read_bool(f)
        self.user_data_size = read_short(f)
        self.user_data_size_bits = read_uchar(f)
        self.compressed_data = read_bool(f)
        for _ in range(0, self.user_data_size):
            read_uchar(f)
        print(self.max_entries)
        print(self.num_entries)
        print(self.data_length_in_bits)
        print(self.is_user_data_fixed_size)
        print(self.user_data_size)
        print(self.user_data_size_bits)

