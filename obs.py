import os
import time
import glob
import threading
import obspython as obs

run = False
wf = "" 
rf = "" 

def script_description():
    return "Demo2Obs by https://github.com/realSaddy"

def script_properties():
    props = obs.obs_properties_create()
    
    rf = obs.obs_properties_add_text(props, "rf", "Recording folder", obs.OBS_TEXT_DEFAULT)
    obs.obs_property_set_long_description(rf, "The recording folder in your settings (must be the same). OBS doesn't allow the script to get it")
    
    wf = obs.obs_properties_add_text(props, "wf", "Watch folder", obs.OBS_TEXT_DEFAULT)
    obs.obs_property_set_long_description(wf, "The folder where bench outputs. Usually TF2_FOLDER/tf/results")

    b = obs.obs_properties_add_button(props,"b1","Start", b_start)
    
    return props

def b_start(props, prop, *arg, **kwargs):
    p = obs.obs_properties_get(props, "b1")
    obs.obs_property_set_description(p, "Stop")
    obs.obs_property_set_modified_callback(p, b_stop) 
    
    wf = obs.obs_properties_get(props, "wf") 
    obs.obs_property_set_enabled(wf, False) 
    
    rf = obs.obs_properties_get(props, "rf") 
    obs.obs_property_set_enabled(rf, False) 
    
    global run
    run = True
    t = threading.Thread(target=busy_thread)
    t.start()
    return True

def b_stop(props, prop, *arg, **kwargs):
    p = obs.obs_properties_get(props, "b1")
    obs.obs_property_set_description(p, "Start")
    obs.obs_property_set_modified_callback(p, b_start) 
    
    rf = obs.obs_properties_get(props, "rf") 
    obs.obs_property_set_enabled(rf, True) 
    
    wf = obs.obs_properties_get(props, "wf") 
    obs.obs_property_set_enabled(wf, True) 
    
    global run 
    run = False
    
    return True

def script_update(settings):
    global wf
    global rf

    wf = obs.obs_data_get_string(settings, "wf")
    rf = obs.obs_data_get_string(settings, "rf")

def busy_thread():
    while run:
        if os.path.exists(wf) and os.path.exists(rf):
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
                else:
                    obs.obs_frontend_recording_start()
                print("file exists, deleting")
        else:
            print("WF/RF PATH DOES NOT EXIST!")
        time.sleep(.1)
