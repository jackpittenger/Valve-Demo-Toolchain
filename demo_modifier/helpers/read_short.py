import struct

def read_short(f):
    return struct.unpack("H", f.read(2))[0]
