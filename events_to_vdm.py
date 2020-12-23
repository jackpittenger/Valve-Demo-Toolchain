# Created by https://github.com/realSaddy
import os
import argparse

parser = argparse.ArgumentParser(description="Demo2Obs by https://github.com/realSaddy", prefix_chars="-+")

parser.add_argument("demos_folder", type=str, help="The directory where your demos and _events.txt is stored")
parser.add_argument("--time_before_killstreak", type=int, help="How long should it record before a killstreak event? (DEFAULT 1000)", default=1000)
parser.add_argument("--time_before_bookmark", type=int, help="How long should it record before a bookmark event? (DEFAULT 1000)", default=1000)
parser.add_argument("--time_after_killstreak", type=int, help="How long should it record before a killstreak event? (DEFAULT 500)", default=500)
parser.add_argument("--time_after_bookmark", type=int, help="How long should it record before a bookmark event? (DEFAULT 500)", default=500)
parser.add_argument("--demos_folder_in_tf", type=str, help="To autoload the next demo you need to specify the demo folder relative to tf. Make sure to have a trailing / (DEFAULT "")", default="")
parser.add_argument("+nochat", help="Disable chat", action="store_true")
parser.add_argument("--custom_start_commands", type=str, help="Custom TF2 commands to run at the start of demos. Don't forget ';'!", default="")
parser.add_argument("--custom_end_commands", type=str, help="Custom TF2 commands to run at the end of demos. Don't forget ';'!", default="")

args = parser.parse_args()

###

def get_header(i):
    return f'\t"{i}"\n\t{{\n'

def get_factory(name):
    return f'\t\tfactory "{name}"\n'

def get_name(event_type, i):
    return f'\t\tname "{event_type}{i+1}"\n'

def get_start_tick(lt, delta=0):
    st = 250 if(lt == 0) else int(lt) + delta
    return f'\t\tstarttick "{st}"\n'

def get_footer():
    return f'\t}}\n'

def add_rec(i, stt, name, event_type, event_type_2, tick, typ):
    ## Start recording
    # Header
    ret = get_header(i)
    # Factory
    ret += get_factory("PlayCommands")
    # Name
    ret += get_name(typ, i)
    # Start Tick
    ret += get_start_tick(stt)
    # Command
    ret += f'\t\tcommands "sv_cheats 1;bench_start REC{typ}.{name}_{event_type}_{event_type_2}_{tick};bench_end;snd_restart;sv_cheats 0;"\n'
    # Footer
    ret += get_footer() 
    return ret

def get_line_info(line):
    s = line.split(" ")
    event_type = s[2]
    event_type_2 = s[3]
    event_tick = s[6].split(")")[0]

    return (event_type, event_type_2, event_tick)

def get_delta(event_type):
    if event_type == "Killstreak":
        return (args.time_after_killstreak, args.time_before_killstreak)
    return (args.time_after_bookmark, args.time_before_bookmark)

def start_stop_commands(name, commands, i=1, tick=200):
    ret = ""
    ret += get_header(i)
    ret += get_factory("PlayCommands")
    ret += get_name(name, i)
    ret += get_start_tick(tick)
    ret += f'\t\tcommands "{";".join(commands)}"\n'
    ret += get_footer()
    return ret

###

with open(args.demos_folder+"/_events.txt", "r") as f:
    r = f.read()
    dems = r.split(">\n")[1:]
    dems = [dem for dem in dems if os.path.exists(args.demos_folder+"/"+dem.split('"')[1]+".dem")]
    for a, dem in enumerate(dems):
        name = dem.split('"')[1]
        output = "demoactions\n{\n"
        lines = dem.split("\n")[:-1]

        # Runs commands at the start
        start_commands = args.custom_start_commands.split(";")
        if args.nochat:
            start_commands.append("hud_saytext_time 0")

        output += start_stop_commands("STARTCMDS", start_commands)
        
        lt = 0
        i = 1
        l = 0
        for line in lines:
            event_type, event_type_2, event_tick = get_line_info(line)
            print("FILE: "+name+" TYPE: "+event_type+" @ TICK: "+event_tick)
            delta_a, delta_b = get_delta(event_type)
            stt = max(251, int(event_tick) - delta_b)    
            
            if stt > lt:
                i += 1
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
                output += f'\t\tskiptotick "{stt}"\n'
                # Footer
                output += get_footer()
                
                # Start recording
                i += 1
                output += add_rec(i, stt, name, event_type, event_type_2, event_tick, "START")
            if len(lines) > l+1:
                n_event_type, n_event_type_2, n_event_tick = get_line_info(lines[l+1]) 
                n_delta_a, n_delta_b = get_delta(n_event_type)
                if int(event_tick) + delta_a < int(n_event_tick)-n_delta_b:
                    # Stop recording
                    i += 1
                    output += add_rec(i, stt+delta_a+delta_b, name, event_type, event_type_2, event_tick, "STOP")
    
            ## Pass data
            l += 1
            lt = stt+delta_b+delta_a

        output += add_rec(i+1, int(lt), name, event_type, event_type_2, event_tick, "STOP")
        
        # End commands
        end_commands = args.custom_end_commands.split(";")
        if args.nochat:
            end_commands.append("hud_saytext_time 12")

        output += start_stop_commands("ENDCMDS", end_commands, i+2, int(lt)+50)
        
        output += get_header(i+3)
        output += get_factory("PlayCommands")
        output += get_name("END", i+3)
        output += get_start_tick(int(lt)+100)
        if(a == len(dems)-1):
            output += f'\t\tcommands "stopdemo"\n'
        else:
            output += f'\t\tcommands "playdemo {args.demos_folder_in_tf}'+dems[a+1].split('"')[1]+'"\n'
        output += get_footer()

        with open(args.demos_folder+"/"+name+".vdm", "w") as c:
            c.write(output+"}\n")
    f.close()

