# Not ready for production! A video guide will come out soon when everything is ready (~1st)
# Valve Demo Toolchain
This collection of tools allow you to perform useful operations on Valve's .dem files, including automatically recording your TF2 Demo files with OBS.

## Tools
### Events to VDM
Transforms your \_events.txt into VDM files that are read by the Source engine.
 
#### Usage
```
python events_to_vdm.py "path/to/demos/folder"
``` 
With
* `"path/to/demos/folder"` as the path to where your demos are located (usually tf).
    
Optionally with
* `--time_before_killstreak int` *(DEFAULT 1000)* Ticks before a killstreak event to start recording.
* `--time_before_bookmark int` *(DEFAULT 1000)* Ticks before a bookmark event to start recording.
* `--time_after_killstreak int` *(DEFAULT 500)* Ticks after a killstreak event to start recording.
* `--time_after_bookmark int` *(DEFAULT 500)* Ticks after a bookmark event to start recording.
* `--demos_folder_in_tf folder/` *(DEFAULT "")* If you have symlinked your demos folder to another path, use this to specify where to look inside tf for the next demo file.
* `+nochat` *(DEFAULT FALSE)* Disable chat replay.
* `--custom_start_commands "commands_seperated by;"` *(DEFAULT "")* Commands to be run at the start of a demo. Takes in "" containing ; separated commands.
* `--custom_end_commands "commands_seperated by;"` *(DEFAULT "")* Commands to be run at the end of a demo. Takes in "" containing ; separated commands.

### Demo2Obs
See [this README](https://github.com/realSaddy/Valve-Demo-Toolchain/tree/master/obs#demo2obs)

## Attribution
Created by [realSaddy](https://saddy.dev).

Thanks to Ryuk for inspiration with [RyukBot](https://www.youtube.com/watch?v=oy023_giJdQ). Please check him out for a solution that utilizes TF2's internal exporter.

Licensed under AGPLv3.
