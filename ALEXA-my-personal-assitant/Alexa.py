try:
    import sqlite3
    import os
    import traceback2 as traceback
    import pyautogui as do
    import time
    import sys
    import playSeries
    import subprocess
    import random
    import pyttsx3
    import speech_recognition as sr
    import psutil
    import datetime
    from dateutil import relativedelta
    import threading
    import requests
    import shedule
    import pickle
    import wikipedia
    import pygame
    from plyer import notification
    import pyjokes
    import pwinput
    import winsound
    import smtplib
    import win32gui
    
    created_date=[21,6,2022]
    KeySound = True
    version="1.2.1"
    voice_rate=150
    connection=sqlite3.connect("C:\\Users\\RAJAN\\Desktop\\Alexa.python.source\\My_Bot.db")
    cursor=connection.cursor()
    global name
    name=False
    shedules={}                   #{"shedule":False,"time_or_hour":"null",'time_1':[0,0],'time_2':[0,0],'hour':[0,0]}
    sql_command=""" SELECT * FROM Bot_Data;"""
    cursor.execute(sql_command)
    fetch_all=cursor.fetchall()[0]
    my_name=fetch_all[1]
    my_gender=fetch_all[2]
    default_browser=fetch_all[3]
    if default_browser=='chrome':
        default_browser_index=1
    elif default_browser=='firefox':
        default_browser_index=0
    input_type=fetch_all[4]
    connection.commit()
    connection.close()
    def updata_Database(title,new_value):
        connection=sqlite3.connect("C:\\Users\\RAJAN\\Desktop\\Alexa.python.source\\My_Bot.db")
        cursor=connection.cursor()
        sql_command=f"""UPDATE Bot_Data SET {title} = "{new_value}";"""
        cursor.execute(sql_command)
        connection.commit()
        connection.close()
    browser=["C:\\Program Files\\Mozilla Firefox\\firefox.exe","C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"]
    engine=pyttsx3.init()
    voices=engine.getProperty('voices')
    engine.setProperty('voice',voices[1].id)              #engine.setProperty('voice',voices[my_gender].id)
    engine.setProperty('rate',voice_rate)
    #updata_Database("MY_NAME","Martina")
    def setFullVolume():
        for i in range(50):
            do.press("volumeup")
    def speak(text,display_text=""):
        if len(display_text)!=0:
            print(f":: {display_text}")
        else:
            print(f":: {text}")
        engine.say(text)
        engine.runAndWait()
    def speak_thread(text,display_text=""):
        thread=threading.Thread(target=speak,args=(text,display_text))
        thread.start()
    def request():
        try:
            requests.get("http://www.example.com",timeout=1)
            return True
        except:
            return False
    def get_command(text):
        if len(text)!=0:
            speak(text)
        if input_type == 'voice':
            if request():
                while True:
                    try:
                        rec=sr.Recognizer()
                        with sr.Microphone() as source:
                            sr.pause_threshold=1
                            print(">> ",end='')
                            audio=rec.listen(source)
                        query=rec.recognize_google(audio,language='en-in')
                        print(f"{query}")
                    except Exception as e:
                        query=False
                        global name
                        name=False
                    if query:
                        break
            else:
                updata_Database("INPUT_TYPE","text")
                speak("Internet: Unavailable\nInput type changed to 'TEXT'")
                #input_type='text'
                sys.exit()
                query=input(">> ")
        else:
            query=""
            while not query:
                query=input(">> ")
        return query
    def change_voice(gender,rate=None):
        if rate is not None:
            engine.setProperty('rate',rate)
        engine.setProperty('voice',voices[gender].id)
    def battery_report():
        battery=psutil.sensors_battery()
        plugged=battery.power_plugged
        percent=battery.percent
        if plugged:
            plugged_status="Power Plugged in"
        else:
            plugged_status="Not Plugged in"
        speak(f"Battery Percentage {percent} % : {plugged_status}")
        if percent<20 and (plugged==False):
            speak("Hey You, Kindly Plug you battery")
        elif percent>97 and (plugged==True):
            speak("Au, Plug your battery Out")
    def get_internet_status():
        try:
            requests.get("http://www.example.com")
            speak("Internet: Connected")
        except:
            speak("Interned: Not Connected")
    def basic_checks():
        pass
    def search_movie(dir_y,movie_name):
        for video in os.listdir(dir_y):
            if (movie_name in video.lower()) and (video.endswith(".mp4") or video.endswith(".mkv")):
                video_new=video.replace("_"," ")
                os.rename(os.path.join(dir_y,video),os.path.join(dir_y,video_new))
                movie_dir=os.path.join(dir_y,video_new)
                return movie_dir
        for F_f in os.listdir(dir_y):
            if os.path.isdir(os.path.join(dir_y,F_f)):
                movie_dir=search_movie(os.path.join(dir_y,F_f),movie_name.lower())
                if movie_dir is not None:
                    return movie_dir
    def printMovies(dir_y,tab):
        global movies_count
        for video in os.listdir(dir_y):
            if os.path.isdir(os.path.join(dir_y,video)):
                for i in range(tab):
                    print('\t',end='')
                print('==>>%s'%(video))
                tab+=1
                printMovies(os.path.join(dir_y,video),tab)
                tab-=1
            else:
                if(video.endswith('.mkv') or video.endswith('.mp4')):
                    movies_count+=1
                    for i in range(tab):
                        print('\t',end='')
                    print('%s'%(video))
        return movies_count
    def save_movie(movie_dir):
        try:
            file=open('C:\\Users\\RAJAN\\Desktop\\Alexa.python.source\\playMovie.Data.txt','a')
        except:
            file=open('C:\\Users\\RAJAN\\Desktop\\Alexa.python.source\\playMovie.Data.txt','w')
        file.write('\n')
        file.write(movie_dir)
        file.close()
    def get_age():
        today=[]
        difference=[]
        now=datetime.datetime.now()
        today=datetime.datetime.strptime(f'{int(now.strftime("%d"))},{int(now.strftime("%m"))},{int(now.strftime("%Y"))}',"%d,%m,%Y")
        created=datetime.datetime.strptime(f'{created_date[0]},{created_date[1]},{created_date[2]}',"%d,%m,%Y")
        differ=relativedelta.relativedelta(today,created)
        days=differ.days
        months=differ.months
        years=differ.years
        if years==0 and months==0 :
            speak(f"I am {days} days old")
        elif years==0:
            speak(f"I am {months} months and {days} days old")
        else:
            speak(f"I am {years} years and {months} months old")
    def continue_movie():
        try:
            file=open('C:\\Users\\RAJAN\\Desktop\\Alexa.python.source\\playMovie.Data.txt','r')
            line=file.readlines()
            last_movie=line[len(file.readlines())-1]
            print(last_movie)
            file.close()
            save_movie(last_movie)
            subprocess.Popen(["C:\\Program Files (x86)\\VideoLAN\VLC\\vlc.exe",last_movie])
            time.sleep(3)
            do.click(x=1296, y=55)
            time.sleep(1)    
            do.click(x=688, y=364)
            do.press("f")
        except:
            print("SORRY Data Not Found")
    def playMovie():
        con_pre_mov=input("Wanna continue previous watched movie >> ").lower()
        if "yes" in con_pre_mov:
            continue_movie()
        else:
            movie_path=search_movie("D:\Movies",input("( # for print all movies)\nEnter Movie name: ").lower())
            print('Directory: "{}"'.format(movie_path))
            if movie_path is None:
                print("INVALID MOVIE NAME ENTERED\n\t\tHere are the available MOVIES !!!\n.................................")
                movies_count=printMovies("D:\Movies",1)
                print("\n................................")
                print(" %d movies are available "%(movies_count))
                playMovie()
            _continue=input("Continuing movie ? ").lower()
            save_movie(movie_path)
            subprocess.Popen(["C:\\Program Files (x86)\\VideoLAN\VLC\\vlc.exe",movie_path])
            time.sleep(2)
            if "yes" in _continue:
                do.click(x=1296, y=55)
            time.sleep(1)    
            do.click(x=688, y=364)
            do.press("f")
    def playVidSong(_any=False):
        directory="D:\VideoSongs"
        if _any:
            folders=os.listdir(directory)
            folders.remove("desktop.ini")
            folder=random.choice(folders)
            name_new=folder#.replace(" ","_")
            #os.rename(os.path.join(directory,folder),os.path.join(directory,name_new))
            folder=name_new
            videos=os.listdir(os.path.join(directory,folder))
            video_name=random.choice(videos)
            new_name=video_name#.replace(" ","_")  
            #os.rename(os.path.join(directory,folder,video_name),os.path.join(directory,folder,new_name))
            video_path=os.path.join(directory,folder,new_name)
            speak(f"Playing video song from {folder}")
        else:
            video_path=search_movie(directory,get_command("Video song name: ").lower())       
            if video_path is None:
                speak("Sorry!")
                playVidSong()
        print(video_path)
        subprocess.Popen([r"""C:\Program Files (x86)\VideoLAN\VLC\vlc.exe""",rf"{video_path}"])
        print('Directory: "{}"'.format(video_path))
        time.sleep(2)
        time.sleep(1)    
        do.click(x=688, y=364)
        do.press("f")
    def check(cmd,*args):
        for i in range(len(args)):
            if args[i] in cmd:
                return True
        return False
    def fixed_time_input(perm):
        _from=get_command("From: ").split()
        to=get_command("To: ").split()
        subprocess.Popen(["C:\\Users\\RAJAN\\Desktop\\Alexa.python.source\\shedule.py",_from[0],_from[1],to[0],to[1]],shell=True)
        if perm:
            try:
                shedules['shedule']=True
                shedules['time_or_hour']='time'
                shedules['time_1']=_from
                shedules['time_2']=to
                shedules['hour']=[0,0]
                data_file=open("shedule_data.dat","wb")
                pickle.dump(shedules,data_file)
                data_file.close()
                speak("Shedule had been set for permanent")
            except Exception as e:
                speak(f"Error {e}")
    def fixed_hour_input(perm):
        hour_minute=get_command("How many hours and minutes do you want to be sheduled ? ").split()
        subprocess.Popen(["C:\\Users\\RAJAN\\Desktop\\Alexa.python.source\\shedule.py",hour_minute[0],hour_minute[1]],shell=True)
        if perm:
            try:
                shedules['shedule']=True
                shedules['time_or_hour']='hour'
                shedules['time_1']=[0,0]
                shedules['time_2']=[0,0]
                shedules['hour']=hour_minute
                data_file=open("shedule_data.dat","wb")
                pickle.dump(shedules,data_file)
                data_file.close()
                speak("Shedule had been set for permanent")
            except Exception as e:
                speak(f"Error {e}")
    def yes(cmd):
        return check(cmd,"yes","yea","si","sure","y")
    def hear():
        return check(cmd,"are","can") and check(cmd,"hear")
    def main(cmd=None):
        _exit=False
        if cmd is None:
            cmd = get_command("").lower()
        def check_name(cmd):
            if my_name.lower() in cmd:
                cmd=cmd.replace(f"{my_name.lower()}","")
            else:
                cmd=check_name(get_command("").lower())
            return cmd
        if input_type=="voice" and len(sys.argv)==1:
            cmd=check_name(cmd)
        #"""###########################################"""
        elif my_name.lower() in cmd:
            cmd=cmd.replace(f"{my_name.lower()}","")
        if check(cmd,"search on web"):                              #command
            if request():
                search=cmd.replace("search on web","")
                subprocess.Popen([browser[default_browser_index],search],shell=True)
                _exit=True
            else:
                speak("Sorry, Internet: Unavailable")
        elif check(cmd,"i am horny","go incognito","lets start"):                           #command_list=['i am horny','go incognito','lets start']
            if request():
                search = input("Search: ")
                subprocess.Popen([browser[default_browser_index]],shell=True)
                time.sleep(5)
                do.hotkey('ctrl','shift','p')
                time.sleep(2)
                do.write(search)
                do.press('enter')
            else:
                speak("Au, Internet: Unavailable")
        elif check(cmd,"fuck you"):
            speak("Fuck you too")
        elif check(cmd,"set","setup","start","make") and check(cmd,"shedul"):             #command  ###############shedule
            if check(cmd,"hour","hour") and check(cmd,"fixed"):
                if check(cmd,"permanent"):
                    fixed_hour_input(True)
                else:
                    fixed_hour_input(False)
            elif check(cmd,"time","timing") and check(cmd,"fixed"):
                if check(cmd,"permanent"):
                    fixed_time_input(True)
                else:
                    fixed_time_input(False)
            else:
                cmd=get_command("Fixed time shedule or fixed hour shedule ?")
                if check(cmd,"time"):
                    if check(cmd,"permanent"):
                        fixed_time_input(True)
                    else:
                        fixed_time_input(False)
                elif check(cmd,"hour"):
                    if check(cmd,"permanent"):
                        fixed_hour_input(True)
                    else:
                        fixed_hour_input(False)
                else:
                    speak("Sorry")
        elif check(cmd,"cancel","destroy","clear") and check(cmd,"shedule"):
            try:
                global shedules
                shedules['shedule']=False
                shedules['time_or_hour']='none'
                shedules['time_1']=[0,0]
                shedules['time_2']=[0,0]
                shedules['hour']=[0,0]
                data_file=open("shedule_data.dat","wb")
                pickle.dump(shedules,data_file)
                data_file.close()
                speak("All your shedules are cleared")
            except Exception as e:
                speak(f"Error {e}")
        elif check(cmd,"time") and check(cmd,"what"):
            if datetime.datetime.now().hour>12:
                hour=datetime.datetime.now().hour-12
                am_pm="PM"
            elif datetime.datetime.now().hour==12:
                hour=datetime.datetime.now().hour
                am_pm="PM"
            else:
                hour=datetime.datetime.now().hour
                am_pm="AM"
            speak(f"Now the time is {hour} : {datetime.datetime.now().minute} {am_pm}")
        elif check(cmd,"date","today") and check(cmd,"what"):
            now=datetime.datetime.now()
            speak(f"Today is {datetime.datetime.now().day} of {now.strftime('%B')}")
        elif check(cmd,"show","get") and check(cmd,"shedule"):
            data_file=open('shedule_data.dat','rb')
            shedules=pickle.load(data_file)
            if shedules['shedule']:
                if shedules['time_or_hour']=='time':
                    _from=shedules['time_1']
                    to=shedules['time_2']
                    speak(f"Your Shedule:\nType: fixed time\nFrom: {_from[0]} {_from[1]}\nTo: {to[0]} {to[1]}")
                elif shedules['time_or_hour']=='hour':
                    hour_minute=shedules['hour']
                    speak(f"Your Shedule:\nType: fixed hour\nTiming: {hour_minute[0]} hours {hour_minute[1]} minutes")
            else:
                speak("Sorry, You have no shedules")
        elif check(cmd,"open") and check(cmd,"your source"):
            threading.Thread(target=speak,args=("Opening Alexa source code...",)).start()
            subprocess.Popen([r"C:\\Program Files\\Python310\\Lib\\idlelib\\idle.pyw",sys.argv[0]],shell=True)
        elif check(cmd,"web") and check(cmd,"design","develop"):      #command
            web_work_folders=['Git']
            for i in range(len(web_work_folders)):
                print("%d) %s"%(i+1,web_work_folders[i]))
            web_folder=input("Enter any file name above > ")
            if web_folder in web_work_folders:
             folder_path=os.path.join("C:\\Users\\RAJAN\\Desktop",web_folder)
             os.system('cmd /c ""C:\Program Files\Microsoft VS Code\Code.exe" "{}""'.format(folder_path))
             do.click()
             do.hotkey("ctrl","k")
             do.hotkey("ctrl","o")
             time.sleep(1)
             do.write(web_folder)
             do.press('tab')
             do.press("enter")
        elif check(cmd,"play"):                 #command   ############# play
            if check(cmd,"movie"):
                playMovie()
            elif 'series' in cmd:                        #command
                def series(cmd):
                    if "next" in cmd:
                        name,season,episode=playSeries.main("next")
                        voice=True
                    elif "continue" in cmd:
                        name,season,episode=playSeries.main("continue")
                        voice=True
                    elif "manual" in cmd:
                        name,season,episode=playSeries.main("select")
                        voice=True
                    else:
                        series(get_command("do you want to continue series or go to next episode?\nOr else you can go manually"))
                        voice=False
                    if voice:
                        speak(f"Playing {name},Season {season},episode {episode}",f"Series name: {name}\nSeason: {season}\nEpisode: {episode}")
                series(cmd)
                _exit=True
            elif check(cmd,"youtube"):
                if request():
                    import pywhatkit
                    search=cmd.replace("play","").replace("youtube","")
                    pywhatkit.playonyt(search)
                else:
                    speak("Au, Internet Unavailable")
            elif check(cmd,"video song"):
                if check(cmd,"any","some"):
                    playVidSong(_any=True)
                else:
                    playVidSong()
            else:
                speak("What to play?")
        elif check(cmd,"joke"):
            if request():
                speak(pyjokes.get_joke(language='en',category='all'))
            else:
                speak("Internet: Unavailable")
        elif 'search' in cmd:                        #command
            if request():
                search = get_command("Search what ? ")
                subprocess.Popen([browser[default_browser_index],search],shell=True)
                time.sleep(5)
                _exit=True
            else:
                speak("Au, Internet: Unavailable")
        elif check(cmd,"capture","take") and check(cmd,"image","photo","picture","selfie","camera"):
            sys.path.append("C:\\Users\\RAJAN\\Desktop\\cv2.python.source")
            import image_capture
            speak("Say, cheeeeese")
            image_dir=image_capture.capture()
            speak("Image captured")
            print(f"Saved at: {image_dir}")
        elif check(cmd,"who is"):
            if request():
                person=cmd[int(cmd.find('who is')+7):]
                try:
                    if 'just' in cmd:
                        speak(wikipedia.summary(person,sentences=1))
                    else:
                        speak(wikipedia.summary(person,sentences=2))
                except NameError:
                    speak(f"I dont know who is {person}")
                except Exception as e:
                    speak(f"Error {e}")
            else:
                speak("Internet: Unavailable")
        elif check(cmd,"last usage"):
            speak(f"Your Last Usage : {lastUsage.get_last_usage()}")
        elif check(cmd,"send") and check(cmd,"mail"):
            def send_mail(receiver,subject,message):
                server=smtplib.SMTP('smtp.gmail.com',587)
                server.starttls()
                server.login("rajanofficial002@gmail.com","#rajan#002#")
                email=EmailMessage()
                email['From']="rajanofficial002@gmail.com"
                email['To']=receiver
                email['Subject']=subject
                email.set_content(message)
                server.send_message(email)
                speak("Mail sent sucessfully")
            def get_mail_info():
                to=get_command("To: ")
                subject=get_command("Subject: ")
                message=get_command("Message")
                if yes(get_command("Sure to send?")):
                    send_mail(to,subject,message)
            speak("Tell me the details")
            get_mail_info()
        elif check(cmd,"key") and check(cmd,"sound"):
            if check(cmd,"on"):
                KeySound=True
                speak("Keyboard sound is Turned On")
            elif check(cmd,"off"):
                KeySound=False
                speak("Keyboard sound is Turned Off")
            else:
                if KeySound:
                    speak("Keyboard sound is On")
                else:
                    speak("Keyboard sound is Off")
        elif 'change' in cmd:                                       #command ###############change
            if 'name' in cmd and 'your' in cmd:
                try:
                    new_name=get_command("What would you like to call me ? ")
                    updata_Database("MY_NAME",new_name)
                    new_gender=get_command("Male or female ?")                
                    if check(new_gender,"male","man","m","boy"):
                        updata_Database("GENDER_OF_NAME",0)
                    elif check(new_gender,"female","woman","girl","f"):
                        updata_Database("GENDER_OF_NAME",1)
                    speak(f"Name changed to {new_name}")
                    sys.exit()
                except Exception as e:
                    speak(f"Error {e}")
            elif 'default browser' in cmd:
                browser_name=get_command("Which browse do you prefer ? ")
                try:
                    if check(browser_name,"chrome","firefox","mozilla") in browser_name:
                        if 'chrome'in browser_name:
                            updata_Database("DEFAULT_BROWSER","chrome")
                            speak("I have changed CHROME as a default Browser")
                        elif ('firefox' or 'mozilla') in browser_name:
                            updata_Database("DEFAULT_BROWSER","firefox")
                            speak("I have changed FIREFOX as a default Browser")
                    else:
                        speak("INVALID BROWSER NAME")
                except:
                    speak("I am done")
            elif check(cmd,"input type"):
                try:
                    if input_type=='text':
                        if request():
                            updata_Database("INPUT_TYPE","voice")
                            speak("Input type changed to 'VOICE'")
                            sys.exit()
                        else:
                            speak("Sorry, Internet is Unavailable")
                    elif input_type=='voice':
                        updata_Database("INPUT_TYPE","text")
                        speak("Input type changed to 'TEXT'")
                        sys.exit()
                except Exception as e:
                    speak(f"Error: {e}")
            elif check(cmd,"video song"):
                subprocess.Popen(["taskkill","/im","vlc.exe"],shell=True)
                playVidSong(_any=True)
            else:
                speak("Sorry")
        elif check(cmd,"what") and check(cmd,"i do"):
            speak("Do, whatever you want to do ? ")
            cmd=get_command("Got bored?")
            if yes(cmd):
                if yes(get_command("Like to watch some Video songs?")):
                    playVidSong()
        elif check(cmd,"what") and check(cmd,"can you do","you can do"):
            speak("I am just learning, Teach me more everyday.\nBy the way i can follow your commands.")
        elif input_type=="voice" and hear():
            speak("Yea, I am hearing you")
        elif check(cmd,"repeat") and check(cmd,"my","me"):                  #command
            speak(get_command("okay, i do repeat"))
        elif check(cmd,"open"," start ","create"):                    #command    ##################open
            def _open(cmd):
                if check(cmd,"cmd","command prompt"):
                    subprocess.Popen(['start'],shell=True)
                elif check(cmd,"chrome"):
                    subprocess.Popen(["C:\Program Files\Google\Chrome\Application\chrome.exe"],shell=True)
                elif 'browser' in cmd:
                    subprocess.Popen([browser[default_browser_index]],shell=True)
                elif check(cmd,"new") and check(cmd,"python"):
                    file_name=get_command("Your file name: ")
                    if file_name.endswith(".py"):
                        pass
                    else:
                        file_name+='.py'
                    for file in os.listdir("C:\\Users\\RAJAN\\Desktop"):
                        if file.endswith(".py"):
                            if file_name == file:
                                print("Bulshit, file already exists !")
                    new_file_path=os.path.join("C:\\Users\\RAJAN\\Desktop",file_name)
                    subprocess.Popen([r"C:\\Program Files\\Python310\\Lib\\idlelib\\idle.pyw",new_file_path],shell=True)
                elif check(cmd,"notes","text","document"):
                    notepad_dir=r"C:\Users\RAJAN\Desktop\Alexa.python.source\Notepads"
                    if check(cmd,"new"):
                        name=get_command("Name your file: ")
                        if len(name)==0:
                            now=datetime.datetime.now()
                            name = now.strftime("%y")+ now.strftime("%m")+now.strftime("%d")+now.strftime("%H")+now.strftime("%M")+now.strftime("%S")
                        if not name.endswith(".txt"):
                            name+=".txt"
                        with open(os.path.join(notepad_dir,name),"w") as file:
                            file.write(get_command("Write your file: "))
                        speak("Your file saved")
                        print("Saved at {os.path.join(os.getcwd,'Notepads',name)}")
                    else:
                        if check(cmd,".txt"):
                            cmd=cmd.split()
                            for text in cmd:
                                if text.endswith(".txt"):
                                    document=text
                            for file in os.listdir(notepad_dir):
                                if file.endswith(".txt") and file.replace(".txt","").lower()==document.replace(".txt","").lower():
                                    with open(os.path.join(notepad_dir,file),"r") as file_wrapper:
                                        speak("Here is your text document:")
                                        print("\n\t\t"," ".join(file_wrapper.readlines()))
                                    print("\n(1) clear and re-write (2) add more text (3) delete (4) close")
                                    options=input("Give any file options: ")
                                    if "del" in options:
                                        os.remove(os.path.join(notepad_dir,file))
                                        speak("File deleted succesfully")
                                    elif check(options,"re","over"):
                                        file_data=get_command("Start writing your file right here:\n\t\t")
                                        with open(os.path.join(notepad_dir,file),"w") as file_wrapper:
                                            file_wrapper.write(file_data)
                                            speak("File saved succesfully")
                                            print(f"Saved at {os.path.join(notepad_dir,file)}")
                                    elif check(options,"update","more","write"):
                                        with open(os.path.join(notepad_dir,file),"r") as file_wrapper:
                                            speak("Continue writing your file: \n\t\t")
                                            existing_data="".join(file_wrapper.readlines())
                                            file_data=input(existing_data)
                                        with open(os.path.join(notepad_dir,file),"w") as file_wrapper:
                                            file_wrapper.write(existing_data+file_data)
                                            speak("File updated succesfully")
                                            print(f"Updated at {os.path.join(notepad_dir,file)}")
                                    else:
                                        speak("File closed")
                                else:
                                    speak("File not found")
                        else:
                            _open(get_command("What is your file name: ")+" document")
                elif check(cmd,"project",".py","python"):
                    def search_python(root_directory,python_file_name):
                        for file in os.listdir(root_directory):
                            if file==python_file_name:
                                directory=os.path.join(root_directory,file)
                                return directory
                        for file in os.listdir(root_directory):
                            if os.path.isdir(os.path.join(root_directory,file)):
                                directory=search_python(os.path.join(root_directory,file),python_file_name)
                                if directory is not None:
                                    return directory
                    cmd=cmd.split()
                    found=False
                    file_name=None
                    for name in cmd:
                        if name.endswith(".py") or name.endswith(".pyw"):
                            python_file_name=name
                            file_name=search_python("C:\\Users\\RAJAN\\Desktop",python_file_name)
                            found=True
                    if not found:
                        python_file_name=get_command("Your file name: ")
                        if python_file_name.endswith(".py") or python_file_name.endswith(".pyw"):
                            file_name=search_python("C:\\Users\\RAJAN\\Desktop",python_file_name)
                        else:
                            speak("This is not a python file")
                    if file_name is not None:
                        if check(cmd,"run","execute"):
                            subprocess.Popen(["start","cmd","/k",file_name],shell=True)
                        else:
                            subprocess.Popen(["C:\Program Files\Python310\Lib\idlelib\idle.pyw",file_name],shell=True)
                        speak(text=f"Opening {python_file_name.replace('_',' ').replace('.py',' dot pi')}",display_text=f"Opening {python_file_name}")
                    else:
                        speak("Invalid file name")
                elif check(cmd,"video songs"):
                    subprocess.Popen(["start","D:\VideoSongs"],shell=True)
                    speak("Here are your Video songs")
                elif check(cmd,"movies"):
                    subprocess.Popen(["start","D:\Movies"],shell=True)
                    speak("Here are your movies")
                elif check(cmd,"web series"):
                    subprocess.Popen(["start","D:\WebSeries"],shell=True)
                    speak("Here are your series")
                elif check(cmd,"python") and check(cmd,"idle"):
                    subprocess.Popen(["C:\Program Files\Python310\Lib\idlelib\idle.pyw"],shell=True)
                    speak("Opening...")
                elif check(cmd,"your") and check(cmd,"source","code"):
                    subprocess.Popen(["C:\\Program Files\\Python310\\Lib\\idlelib\\idle.pyw",sys.argv[0]],shell=True)
                    speak("Opening my source...")
                elif check(cmd,"setting") and check(cmd,"bluetooth"):
                    do.press("win")
                    time.sleep(1)
                    do.write("bluetooth")
                    time.sleep(1)
                    do.press("enter")
                else:
                    speak("What to open ?")
            _open(cmd)
        elif check(cmd,"rerun"):
            subprocess.Popen(["start","cmd","/k",sys.argv[0]],shell=True)
            speak("Restarting Alexa program...")
            os.system("exit")
            sys.exit()
        elif check(cmd,"connect","link"):
            if check(cmd,"bluetooth"):
                pass
            elif check(cmd,"wifi"):
                def wifi(cmd):
                    def connect_wifi(name):
                        speak(f"Connecting to {name} ...")
                        out=str(subprocess.run(["netsh","wlan","connect","name","=",name],shell=True,capture_output=True).stdout)
                        if "not available" in out:
                            speak("Network not available")
                        elif "completed successfully" in out:
                            speak("Wifi connected")
                        else:
                            speak("Error occured while connecting {name}")
                    wifi_dictionary={"rajan":"Galaxy M02s","daddy":"vivo 1909","mummy":"Galaxy J7 DuoC5D7"}
                    names = [key for key in wifi_dictionary]
                    invalid=True
                    for index,name in enumerate(names):
                        if name in cmd:
                            connect_wifi(wifi_dictionary[name])
                            invalid=False
                    if invalid:
                        connect_wifi(wifi_dictionary["rajan"])
                wifi(cmd)
            else:
                pass
        elif check(cmd,"close","quit","destroy","terminate","crash","exit"):         #command      ###############close
            def close_function(cmd):
                force=False
                if check(cmd,"cmd","command prompt") :
                    taskname='cmd.exe'
                elif check(cmd,"vlc","video player","media player"):
                    taskname='vlc.exe'
                elif check(cmd,"python"):
                    if check(cmd,"background","pythonw"):
                        taskname="pythonw.exe"
                        force=True
                    elif check(cmd,"idle"):
                        taskname="idle.pyw"
                    else:
                        taskname="python.exe"
                elif 'browser' in cmd:
                    taskname='chrome.exe'
                elif check(cmd,"vbs","wscript"):
                    taskname="wscript.exe"
                else:
                    taskname=None
                if taskname is not None:
                    try:
                        if not force:
                            subprocess.Popen(['taskkill','/im',taskname],shell=True)
                        else:
                            subprocess.Popen(['taskkill','/f',taskname],shell=True)
                        speak(f"{taskname.replace('.exe','')} Closed")
                    except Exception as e:
                        speak(e)
                else:
                    cmd=get_command("What to close?").lower()
                    close_function(cmd)
            close_function(cmd)
        elif check(cmd,'internet'):                     #command
            get_internet_status()
        elif check(cmd,'how many line') and check(cmd,"you"):
            my_file=open(sys.argv[0],'r')
            lines=my_file.readlines()
            speak(f"I am {my_name} and i am coded for {len(lines)} lines, In Python")
            my_file.close()
        elif 'battery' in cmd:                                      #command
           battery_report()
        elif check(cmd,"you","your") and check(cmd,"born","birth","create","dob"):
            speak(f"I was created on {created_date[0]} {created_date[1]} {created_date[2]}, using PYTHON")
        elif check(cmd,"restart mode"):
            file=open("startup.data.txt","w")
            file.write("message Restart checkup\nNone")
            file.close()
            main("rerun")
        elif check(cmd,"your") and check(cmd,"name"):               #command
            speak(f"My name is {my_name}")
        elif check(cmd,"how","what","age","old") and check(cmd,"you","your"):
            get_age()                                                                                #command
        elif check(cmd,"take me") and check(cmd,"dark"):
            speak("Recuerdar esas canciones ?")
            if pwinput.pwinput(prompt="> ") == "no tengo tiempo para recordar esa canciones":
                speak("Sure, now you are in")
                thread = threading.Thread(target=speak,args=("Authenticating present user ...",))
                thread.start()
        elif check(cmd,"hello","hi","hey"):                       #command
            speak("Hello, Raaajan. How you doing?",display_text="Hello, Rajan. How you doing?")
            get_command("")
            speak("That's better")
        elif check(cmd,"who") and check(cmd,"you"):
            speak(f"By the way, I am {my_name}, your Computer Assistant")
        elif check(cmd,"shutdown"):                                   #commmand
            subprocess.Popen(["start","cmd","/k","C:\\Users\\RAJAN\\Desktop\\Alexa.python.source\\SHUTDOWN_trace_your_path.py"],shell=True)
            sys.exit()
        elif check(cmd,"rerun"):
            subprocess.Popen(["start","cmd","/k",sys.argv[0]],shell=True)
            sys.exit()
        elif check(cmd,"bye"):
            speak("Okay Byee, then")
            sys.exit()
        else:
            global timeout
            if timeout==0:
                speak("Hey you, Bulshit. I am leaving.")
                sys.exit()
            global did_not_catch
            if did_not_catch==0:
                speak("Sorry")
                did_not_catch+=1
            else:
                if did_not_catch%2==0:
                    speak("Oh, Just give the command Properly")
                    did_not_catch+=1
                    timeout-=1
                else:
                    speak("Sorry")
                    did_not_catch+=1
        basic_checks()
        if not _exit:
            main()
    def start(_speak=False):
        basic_checks()
        change_voice(1)
        if is_playing:
            pygame.mixer.music.stop()
            winsound.Beep(1400,200)
        if _speak:
            speak(f"Hello I am {my_name} version {version}. How can i help you  ?",display_text=f"Hello I am {my_name} version: {version}. How can i help you  ?\n")
        else:
            print(f":: Hello I am {my_name} version: {version}. How can i help you  ?\n")
        global did_not_catch
        did_not_catch=0
        global timeout
        timeout=3
        global not_respondig
        not_responding=3
        main()
    #program begins here
    if len(sys.argv)>1:
        main(cmd=sys.argv[1])
    elif __name__=="__main__":
        os.system('color 02')
        os.system(f'title {my_name} {version}')
        name_len=len(f"{my_name} {version}")
        for i in range(name_len+10):
            print("O",end="")
        print("\n#",end="")
        for i in range(name_len+8):
            print(" ",end="")
        print("#\n#",end="")
        for i in range(4):
            print(" ",end="")
        print(f"{my_name} {version}",end="")
        for i in range(4):
            print(" ",end="")
        print("#\n#",end="") 
        for i in range(name_len+8):
            print(" ",end="")
        print("#")
        for i in range(name_len+10):
            print("O",end="")
        print()
        movies_count=0
        connection=sqlite3.connect("ShutdownDB.db")
        cursor=connection.cursor()
        message="testing message for first"
        open_type="tesging open type for first"
        open_adress="testing open adress for first"
        command="""SELECT * FROM SHUTDOWN"""
        output=cursor.execute(command)
        _all=output.fetchall()
        database=_all[len(_all)-1]
        ID=int(database[0])
        message=str(database[1])
        open_type=str(database[2])
        open_adress=str(database[3])
        power=str(database[4])
        command="""UPDATE SHUTDOWN SET POWER="ON" WHERE ID=ID;"""
        cursor.execute(command)
        connection.commit()
        connection.close()
        if power=="ON":
            print(f"Input Type: {input_type.upper()}")
            if request():
                print("Internet: Available")
            else:
                print("Internet: Unavailable")
            print()
            is_playing=False
            start()
        elif power=="OFF":
            #playing audio      >>>>>>>
            pygame.init()
            pygame.mixer.init()
            pygame.mixer.music.load(r"C:\Users\RAJAN\Desktop\Alexa.python.source\audio.mp3")
            pygame.mixer.music.play()
            is_playing=True
            #<<<<<<<<<<<
            change_voice(0)      #  male - 0   # female - 1
            setFullVolume()
            speak("Hello there!")
            speak(f"Input Type: {input_type.upper()}")
            get_internet_status()
            data_file=open('shedule_data.dat','rb')
            shedules=pickle.load(data_file)          #{"shedule":False,"time_or_hour":"null",'time_1':[0,0],'time_2':[0,0],'hour':[0,0]}
            battery_report()
            basic_checks()
            data_file.close()
            speak(f"Your message:\n\n\t\t{message}\n")
            if shedules['shedule']:
                if shedules['time_or_hour']=='time':
                    _from=shedules['time_1']
                    to=shedules['time_2']
                    subprocess.Popen(["C:\\Users\\RAJAN\\Desktop\\Alexa.python.source\\shedule.py",_from[0],_from[1],to[0],to[1]],shell=True)
                elif shedules['time_or_hour']=='hour':
                    hour_minute=shedules['hour']
                    subprocess.Popen(["C:\\Users\\RAJAN\\Desktop\\Alexa.python.source\\shedule.py",hour_minute[0],hour_minute[1]],shell=True)
            try:
                if open_type=="python":
                    threading.Thread(target=speak,args=(f"Opening python file {os.path.basename({open_adress})}",)).start()
                    subprocess.Popen([r"C:\\Program Files\\Python310\\Lib\\idlelib\\idle.pyw",open_adress],shell=True)
                    winsound.Beep(1400,150)
                    sys.exit()
                elif open_type=="series":
                    if open_adress=="continue":
                        name,season,episode=playSeries.main1(1)
                    elif open_adress=="next":
                        name,season,episode=playSeries.main2()
                    winsound.Beep(1400,150)
                    threading.Thread(target=speak,args=(f"Playing series {name} \nSeason: {season} \nEpisode: {episode}",))
                    sys.exit()
                elif open_type=="movie":
                    threading.Thread(target=speak,args=(f"Playing movie {os.path.basename({open_adress})}",)).start()
                    subprocess.Popen([r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe",f"{open_adress}"],shell=True)
                    winsound.Beep(1400,150)
                    sys.exit()
            except Exception as e:
                speak(f"Error while opening startup file {open_type} ({e})")
            is_playing=True
            start(True)
except Exception as e:
    alexa=r"Alexa.py - C:\Users\RAJAN\Desktop\Alexa.python.source\Alexa.py"
    winsound.Beep(1400,600)
    winsound.Beep(1400,600)
    for trace in traceback.format_exc().split("\n"):
          if str(sys.argv[0]) in trace:
              main_line=trace
    for name in main_line.split(","):
        if "line" in name:
            line=name.split()[-1]
    trace=sys.exc_info()
    notification.notify(title="Error occured in Alexa",message=f"{str(trace[0])[1:-1].replace('class','')} : {line} : {trace[1]}",app_name="Python.exe",timeout=10)
    if alexa in win32gui.GetWindowText(win32gui.GetForegroundWindow()):               #foreground
        do.hotkey("win","up")
    else:
        def getWindow():
            #win32gui.GetWindowText(win32gui.GetForegroundWindow())
            found_alexa=False
            global alexa
            for window in do.getAllWindows():
                if str(alexa) in window.title:
                    alexa=window._hWnd
                    found_alexa=True
            if found_alexa:                                                             #background
                win32gui.SetForegroundWindow(alexa)
                time.sleep(0.8)
                do.hotkey("win","up")
            else:                                                                        #not found
                subprocess.Popen([r"C:\\Program Files\\Python310\\Lib\\idlelib\\idle.pyw",sys.argv[0]],shell=True)
                time.sleep(4)
                getWindow()
        getWindow()
    change_voice(1,rate=220)
    speak("Crashing Alexa Program")
    change_voice(0,rate=250)
    speak(f"Class: {str(trace[0])[1:-1].replace('class','')}")
    speak(f"Line: {line}")
    change_voice(0,150)
    speak(f"{trace[1]}")
    while True:
        pass
