# Created by https://github.com/realSaddy
import os
import struct
import argparse

parser = argparse.ArgumentParser(description="Perform various functions on demo(s), by https://github.com/realSaddy")

parser.add_argument("demo", type=str, help="The demo to perform the operations on")

args = parser.parse_args()

### Helpers

def read_int(f, n=4):
    return struct.unpack("i", f.read(n))[0]

def read_float(f, n=4):
    return struct.unpack("f", f.read(n))[0]

def read_string(f, n=260):
    return f.read(n).strip(b"\x00")

###

### Main functions

def get_header(f):
    dem_protocol = read_int(f) 
    net_protocol = read_int(f)
    host_name = read_string(f)
    client_name = read_string(f)
    map_name = read_string(f)
    gamedir = read_string(f)
    time = read_float(f)
    ticks = read_int(f)
    frames = read_int(f)


    print("Dem Protocol: "+str(dem_protocol))
    print("Net Protocol: "+str(net_protocol))
    print("Host Name: "+str(host_name))
    print("Client Name: "+str(client_name))
    print("Map Name: "+str(map_name))
    print("Game Dir: "+str(gamedir))
    print("Time: "+str(time))
    print("Ticks: "+str(ticks))
    print("Frames: "+str(frames))
    
###

if os.path.exists(args.demo) and args.demo[-4:] == ".dem":
    f = open(args.demo, "rb")
    if read_string(f, 8) != b"HL2DEMO":
        print("ERROR: Invalid header!")
    else:
        get_header(f)
else:
    print("ERROR: Invalid file!")
