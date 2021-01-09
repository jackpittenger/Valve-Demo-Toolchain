import struct

def read_bool(f):
    return struct.unpack("?", f.read(1))
