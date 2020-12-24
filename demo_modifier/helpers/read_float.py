import struct

def read_float(f, n=4):
    return struct.unpack("f", f.read(n))[0]

