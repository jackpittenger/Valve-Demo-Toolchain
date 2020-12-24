import struct

def read_char(f):
    return ord(struct.unpack("c", f.read(1))[0])

