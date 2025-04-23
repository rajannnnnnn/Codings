import time
import pyttsx3
import requests

engine=pyttsx3.init()
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)      #engine.setProperty('voice',voices[my_gender].id)                            
engine.setProperty('rate',130)
def speak(text):
    print(f":{text}")
    engine.say(text)
    engine.runAndWait()

def request():
    try:
        requests.get("http://www.example.com",timeout=5)
        return True
    except:
        return False
def get_Internet():
    if request():
        speak(":Internet: Connected")
        time.sleep(5)
        destroy_Internet()
    else:
        time.sleep(5)
        get_Internet()
def destroy_Internet():
    if not request():
        speak(":Internet: Disconnected")
        time.sleep(4)
        get_Internet()
    else:
        time.sleep(5)
        destroy_Internet()
def start():
    if request():
        destroy_Internet()
    else:
        get_Internet()
start()
