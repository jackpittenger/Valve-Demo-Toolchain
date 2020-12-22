# Created by https://github.com/realSaddy
import os
import argparse

parser = argparse.ArgumentParser(description="Demo2Obs by https://github.com/realSaddy")

parser.add_argument("demos_folder", type=str, help="The directory where your demos and _events.txt is stored")
parser.add_argument("--time_before_killstreak", type=int, help="How long should it record before a killstreak event? (DEFAULT 1000)", default=1000)
parser.add_argument("--time_before_bookmark", type=int, help="How long should it record before a bookmark event? (DEFAULT 1000)", default=1000)
parser.add_argument("--time_after_killstreak", type=int, help="How long should it record before a killstreak event? (DEFAULT 500)", default=500)
parser.add_argument("--time_after_bookmark", type=int, help="How long should it record before a bookmark event? (DEFAULT 500)", default=500)
parser.add_argument("--demos_folder_in_tf", type=str, help="To autoload the next demo you need to specify the demo folder relative to tf. Make sure to have a trailing / (DEFAULT "")", default="")

args = parser.parse_args()

###

def get_header(i):
    return f'\t"{i+1}"\n\t{{\n'

def get_factory(name):
    return f'\t\tfactory "{name}"\n'

def get_name(event_type, i):
    return f'\t\tname "{event_type}{i+1}"\n'

def get_start_tick(lt, delta=0):
    st = 250 if(lt == 0) else int(lt) + delta
    return f'\t\tstarttick "{st}"\n'

def get_footer():
    return f'\t}}\n'

def add_rec(i, stt, name, event_type, event_type_2, tick):
    ## Start recording
    # Header
    ret = get_header(i+1)
    # Factory
    ret += get_factory("PlayCommands")
    # Name
    ret += get_name("REC", i)
    # Start Tick
    ret += get_start_tick(stt)
    # Command
    ret += f'\t\tcommands "sv_cheats 1;bench_start REC.{name}_{event_type}_{event_type_2}_{tick};bench_end;snd_restart;sv_cheats 0;"\n'
    # Footer
    ret += get_footer() 
    return ret

###

with open(args.demos_folder+"/_events.txt", "r") as f:
    r = f.read()
    dems = r.split(">\n")[1:]
    for a, dem in enumerate(dems[:2]):
        name = dem.split('"')[1]
        output = "demoactions\n{\n"
        lines = dem.split("\n")[:-1]
        lt = 0
        i = 0
        for line in lines:
            s = line.split(" ")
            event_type = s[2]
            event_type_2 = s[3]
            event_tick = s[6].split(")")[0]
            print("FILE: "+name+" TYPE: "+event_type+" @ TICK: "+event_tick)
                
            if event_type == "Killstreak":
                delta_a = args.time_after_killstreak
                delta_b = args.time_before_killstreak
            else:
                delta_a = args.time_after_bookmark
                delta_b = args.time_before_bookmark
            
            ## Skip to 
            # Header
            output += get_header(i) 
            # Factory
            output += get_factory("SkipAhead")
            # Name
            output += get_name(event_type, i)
            # Start Tick
            output += get_start_tick(lt) 
            # Skip to Tick
            stt = max(251, int(event_tick) - delta_b)    
            output += f'\t\tskiptotick "{stt}"\n'
            # Footer
            output += get_footer() 
            
            # Start recording
            output += add_rec(i, stt, name, event_type, event_type_2, event_tick)

            # Stop recording
            output += add_rec(i+1, stt+delta_b+delta_a, name, event_type, event_type_2, event_tick)
            
            ## Pass data
            i += 3 
            lt = stt+delta_b+delta_a

        output += get_header(i)
        output += get_factory("PlayCommands")
        output += get_name("END", len(lines))
        output += get_start_tick(int(lt)+100)
        if(a == len(dems)-1):
            output += f'\t\tcommands "stopdemo"\n'
        else:
            output += f'\t\tcommands "playdemo {args.demos_folder_in_tf}'+dems[a+1].split('"')[1]+'"\n'
        output += get_footer()

        with open(args.demos_folder+"/"+name+".vdm", "w") as c:
            c.write(output+"}\n")
    f.close()

