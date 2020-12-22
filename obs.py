# Created by https://github.com/realSaddy
import os
import time
import glob
import threading
import obspython as obs

run = False
wf = "" 
rf = "" 
cb = False
df = ""
af = ""

def script_description():
    return "Demo2Obs by https://github.com/realSaddy"

def visible_prop(props, a, b):
    x = obs.obs_properties_get(props, a)
    obs.obs_property_set_enabled(x, b)

def script_properties():
    props = obs.obs_properties_create()
    
    rf = obs.obs_properties_add_text(props, "rf", "Recording folder", obs.OBS_TEXT_DEFAULT)
    obs.obs_property_set_long_description(rf, "The recording folder in your settings (must be the same). OBS doesn't allow the script to get it")
    
    wf = obs.obs_properties_add_text(props, "wf", "Watch folder", obs.OBS_TEXT_DEFAULT)
    obs.obs_property_set_long_description(wf, "The folder where bench outputs. Usually TF2_FOLDER/tf/results")

    # Auto-move completed demos
    cb_b = obs.obs_properties_add_bool(props, "cb", "Auto-move completed demos?")
    obs.obs_property_set_long_description(cb_b, "Enabling will move recorded .dem, .json, & .vdm files to the archive folder directory to avoid double recording")
    obs.obs_property_set_modified_callback(cb_b, cb_pressed)
    
    df = obs.obs_properties_add_text(props, "df", "Demo folder", obs.OBS_TEXT_DEFAULT)
    obs.obs_property_set_long_description(df, "The folder containing your .dem files")
    visible_prop(props, "df", cb)

    af = obs.obs_properties_add_text(props, "af", "Archive folder", obs.OBS_TEXT_DEFAULT)
    obs.obs_property_set_long_description(af, "The folder to move completed .dem files")
    visible_prop(props, "af", cb)

    b = obs.obs_properties_add_button(props,"b1","Start", b_start)
    
    return props

def cb_pressed(props, prop, *arg, **kwargs):
    visible_prop(props, "df", cb)
    visible_prop(props, "af", cb)
    return True

def b_start(props, prop, *arg, **kwargs):
    p = obs.obs_properties_get(props, "b1")
    obs.obs_property_set_description(p, "Stop")
    obs.obs_property_set_modified_callback(p, b_stop) 
    
    visible_prop(props, "wf", False)
    visible_prop(props, "rf", False)
    
    global run
    run = True
    t = threading.Thread(target=busy_thread)
    t.start()
    return True

def b_stop(props, prop, *arg, **kwargs):
    p = obs.obs_properties_get(props, "b1")
    obs.obs_property_set_description(p, "Start")
    obs.obs_property_set_modified_callback(p, b_start) 
    
    visible_prop(props, "wf", True)
    visible_prop(props, "rf", True)
    
    global run 
    run = False
    
    return True

def script_update(settings):
    global wf
    global rf
    global cb
    global df
    global af

    wf = obs.obs_data_get_string(settings, "wf")
    rf = obs.obs_data_get_string(settings, "rf")
    cb = obs.obs_data_get_bool(settings, "cb")
    df = obs.obs_data_get_string(settings, "df")
    af = obs.obs_data_get_string(settings, "af")

def move_file(clip_name):
    file_types = [".dem", ".json", ".vdm"]

    for t in file_types:
        try:
            f = df + "/" + clip_name + t
            sf = af + "/" + clip_name + t
            if(os.path.exists(f)):
                os.rename(f, sf)
                print("Moved "+f+" TO "+sf)
            else:
                print("--ERROR: Clip "+f+" doesn't exist!")
        except Exception as e:
            print("--ERROR moving file: "+e)
    

def busy_thread():
    obs.obs_frontend_recording_stop()
    while run:
        if not os.path.exists(wf):
            print("--ERROR: Watch folder doesn't exist!")
        elif not os.path.exists(rf):
            print("--ERROR: Record folder doesn't exist!")
        else:
            res = [fn for fn in os.listdir(wf) if fn.startswith("rec.")]
            if(len(res) > 0):
                os.remove(wf+"/"+res[0])
                if obs.obs_frontend_recording_active():
                    obs.obs_frontend_recording_stop()
                    newest = max(glob.glob(rf+"/*"), key=os.path.getctime)
                    newsplit = newest.split("/")
                    filename = "/".join(newsplit[:-1]) + "/" + res[0].split(".")[1] + "." + newsplit[-1].split(".")[1]
                    os.rename(newest, filename)
                    print("Recorded "+filename)
                    if(cb):
                        if not os.path.exists(df):
                            print("--ERROR: Demo folder doesn't exist!")
                        elif not os.path.exists(af):
                            print("--ERROR: Archive folder doesn't exist!")
                        else:
                            move_file("_".join(res[0].split(".")[1].split("_")[:2]))            
                else:
                    obs.obs_frontend_recording_start()
                print("REC Detected")
        time.sleep(.1)
