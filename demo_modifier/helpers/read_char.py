import struct

def read_char(f):
    return ord(struct.unpack("c", f.read(1))[0])

def read_uchar(f):
    return struct.unpack("B", f.read(1))[0]
