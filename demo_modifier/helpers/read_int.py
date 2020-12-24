import struct

def read_int(f, n=4):
    return struct.unpack("i", f.read(n))[0]

