import struct

def read_string(f, n=260):
    return f.read(n).strip(b"\x00")

