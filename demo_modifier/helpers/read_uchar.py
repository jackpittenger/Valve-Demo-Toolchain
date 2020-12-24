import struct

def read_uchar(f, n):
    return list(struct.iter_unpack("H", f.read(n)))

