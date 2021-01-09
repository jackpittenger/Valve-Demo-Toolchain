# Created by https://github.com/realSaddy
import os
import sys
import struct
import argparse

parser = argparse.ArgumentParser(description="Perform various functions on demo(s), by https://github.com/realSaddy")

parser.add_argument("demo", type=str, help="The demo to perform the operations on")

args = parser.parse_args()

from functions.header import get_header
from functions.dem_signon import Dem_Signon
from functions.dem_datatables import Dem_Datatables
from functions.dem_stringtables import Dem_Stringtables

from helpers.read_string import read_string
from helpers.read_char import read_char
from helpers.read_int import read_int

if os.path.exists(args.demo) and args.demo[-4:] == ".dem":
    f = open(args.demo, "rb")
    if read_string(f, 8) != b"HL2DEMO":
        print("ERROR: Invalid header!")
    else:
        get_header(f, True)
        # Cmd Header
        for i in range(0, 8):        
            cmd_type = read_char(f)
            tick = read_int(f)
            
            print("Type: "+str(cmd_type))
            print("Tick: "+str(tick))
            if cmd_type == 1:
                Dem_Signon(f)
            elif cmd_type == 3:
                pass
            elif cmd_type == 6:
                Dem_Datatables(f)
            elif cmd_type == 8:
                Dem_Stringtables(f)
else:
    print("ERROR: Invalid file!")
