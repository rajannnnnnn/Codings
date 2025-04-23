import winsound
import os
from playsound import playsound
import pyttsx3
import psutil
import time
from plyer import notification
import threading

engine=pyttsx3.init()
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)      #engine.setProperty('voice',voices[my_gender].id)                            
engine.setProperty('rate',130)
done=False
def timer():
    global done
    time.sleep(300)
    done=False
def speak(text):
    print(f":{text}")
    engine.say(text)
    engine.runAndWait()
def notify(dry):
    global done
    if not done:
        if not dry:
            message="Au, Plug your battery Out"
        else:
            message="Hey You, Kindly Plug your battery"
        notification.notify(title="Python Battery manager",message=message,app_name="Python.exe",timeout=10)
        done=True
        threading.Thread(target=timer).start()
def battery_check():
    global unplug
    global plug
    battery=psutil.sensors_battery()
    plugged=battery.power_plugged
    percent=battery.percent
    if percent<20 and (plugged==False):
        notify(True)
        unplug=0
        speak("Hey You, Kindly Plug your battery")
        plug+=1
        if plug>4:
            #playsound.playsound("audio.mp3")
            pass
    elif percent>97 and (plugged==True):
        notify(False)
        plug=0
        speak("Au, Plug your battery Out")
        unplug+=1
        if unplug>4:
            #playsound.playsound("audio.mp3")
            pass
    else:
        notification=False
        
plug=0
unplug=0
while True:
    battery_check()
    time.sleep(30)
