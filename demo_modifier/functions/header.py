from helpers.read_int import read_int 
from helpers.read_string import read_string
from helpers.read_float import read_float 

def get_header(f, p):
    dem_protocol = read_int(f) 
    net_protocol = read_int(f)
    host_name = read_string(f)
    client_name = read_string(f)
    map_name = read_string(f)
    gamedir = read_string(f)
    time = read_float(f)
    ticks = read_int(f)
    frames = read_int(f)
    signon = read_int(f)

    if p:
        print("Dem Protocol: "+str(dem_protocol))
        print("Net Protocol: "+str(net_protocol))
        print("Host Name: "+str(host_name))
        print("Client Name: "+str(client_name))
        print("Map Name: "+str(map_name))
        print("Game Dir: "+str(gamedir))
        print("Time: "+str(time))
        print("Ticks: "+str(ticks))
        print("Frames: "+str(frames))
        print("Initial signon: "+str(signon))

