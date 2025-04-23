from plyer import notification
import math
from datetime import datetime
import time
import os
import pyttsx3
import Alexa
import threading
import subprocess
import sys

def get_command(query):
    return Alexa.get_command(query)
now=datetime.now()
engine=pyttsx3.init()
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)              #engine.setProperty('voice',voices[my_gender].id)
engine.setProperty('rate',130)
def speak(text,notify=False):
    if notify:
        notification.notify(title="Shedule",message=text,timeout=0)
    print(f":{text}")
    engine.say(text)
    engine.runAndWait()
    return 0
def time_up():
    speak("Time Up: Your have 5 minutes to Shutdown",True)
    time.sleep(300)
    speak("Time up",True)   #"C:\Program Files\Python310\SHUTDOWN_trace_your_path.py"
    subprocess.Popen(["start","cmd","/k","C:\\Users\\RAJAN\\Desktop\\Alexa.python.source\\SHUTDOWN_trace_your_path.py"],shell=True)
def start_running(shedule_min):
    hour=int(shedule_min)//60
    minute=int(shedule_min)%60
    if hour==0:
        speak(f"You gonna work for {minute} minutes ")
    elif minute==0:
        speak(f"You gonna work for {hour} hour ")
    else:
        speak(f"You gonna work for {round(hour)} hour {minute} minutes")
    remaining=shedule_min
    while remaining!=0:
        if remaining%30==0:                     #for every half an hour
            rem_hour=remaining//60
            rem_minute=remaining%60
            if rem_hour==0:
                speak(f"{rem_minute} minutes remaining",True)
            elif rem_minute==0:
                speak(f"{rem_hour} hour remaining",True)
            else:
                speak(f"{rem_hour} hour {rem_minute} minutes remaining",True)
        time.sleep(60)
        remaining-=1
    time_up()
def check_delay(begin,now_):
    diff=[]
    delay_limit=10   #minutes
    for i in range(2):
        diff.append(now_[i]-begin[i])
    delay=(diff[0]*60)+diff[1]
    return delay
def fixed_time_shedule(begin,end):
    diff=[]
    now_=[]
    time_validated=False
    begin[0]=int(begin[0])
    begin[1]=int(begin[1])
    end[0]=int(end[0])
    end[1]=int(end[1])
    if begin[0]>0 and begin[0]<=24:
        if end[0]>0 and end[0]<=24:
            if begin[1]>=0 and begin[1]<=60:
                if end[1]>=0 and end[1]<=60:
                    if end[0]-begin[0]>0 or end[1]-begin[1]>29:             #validating time
                        time_validated=True
    if time_validated:
        now_.append(int(now.strftime("%H")))
        now_.append(int(now.strftime("%M")))
        for i in range(2):
            diff.append(end[i]-now_[i])
        shedule_min=(diff[0]*60)+diff[1]            #converting to minutes
        delay=check_delay(begin,now_)
        if delay>0 and delay<10:
            start_running(shedule_min)
        elif delay<=0 and delay>-10:
            speak(f"You have come {round(math.sqrt(delay**2))} minutes Sooner")
            start_running(shedule_min)
        else:
            speak("You are out of time: Could not run the desired Shedule")
    else:
        speak("Invalid Time")
def fixed_hour_shedule(hour_min):
    hour_min[0]=int(hour_min[0])
    hour_min[1]=int(hour_min[1])
    shedule_min=(hour_min[0]*60)+hour_min[1]
    start_running(shedule_min)
if len(sys.argv)==3:
    fixed_hour_shedule([sys.argv[1],sys.argv[2]])
elif len(sys.argv)==5:
    fixed_time_shedule([sys.argv[1],sys.argv[2]],[sys.argv[3],sys.argv[4]])
