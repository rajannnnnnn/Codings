##import sqlite3
##connection=sqlite3.connect("ShutdownDB.db")
##cursor=connection.cursor()
##message="testing message for first"
##open_type="tesging open type for first"
##open_adress="testing open adress for first"
###command=f"""CREATE TABLE SHUTDOWN(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,MESSAGE VARCHAR(300),OPEN_TYPE VARCHAR(20),OPEN_ADRESS VARCHAR(100),POWER VARCHAR(10))"""
###command=f"""INSERT INTO SHUTDOWN(MESSAGE,OPEN_TYPE,OPEN_ADRESS,POWER) VALUES ("{message}","{open_type}","{open_adress}","OFF");"""
##command="""SELECT * FROM SHUTDOWN"""
##fetchall=cursor.execute(command)
##print(fetchall.fetchall()[1])
##connection.commit()
##connection.close()
##print("ejhow")
def speak(text):
    Alexa.speak(text)
try:
    import pyttsx3
    import os
    import time
    import sys
    import Alexa
    import threading
    import winsound
    import sqlite3
    import subprocess
    os.system("title Shutdown window")
    os.system("color 02")
    set=Alexa.get_command(":Wanna set next startup purpose, before shutdown ? ")
    next_due=0
    movies_count=0
    def check(cmd,*args):
        for i in range(len(args)):
            if args[i] in cmd:
                return True
        return False
    engine=pyttsx3.init()
    voices=engine.getProperty('voices')
    engine.setProperty('voice',voices[1].id)              #engine.setProperty('voice',voices[1].id)                
    engine.setProperty('rate',200)
    def speak(text):
        print(f":{text}")
        engine.say(text)
        engine.runAndWait()
    power_off="C:\\Users\\RAJAN\\Desktop\\Alexa.python.source\\powerOff.py"
    def countdown():
        speak("System processing Shutdown")
        #threading.Thread(target=winsound.Beep,args=(1100,1000)).start()    
        for i in range(5,0,-1):
            speak(i)
        winsound.Beep(1100,1000)
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
    def search_movie(dir_y,movie_name):
        for video in os.listdir(dir_y):
            if (movie_name in video.lower()) and (video.endswith(".mp4") or video.endswith(".mkv")):
                #new_name=video.replace(" ","_")
                #os.rename(os.path.join(dir_y,video),os.path.join(dir_y,new_name))
                #movie_dir=os.path.join(dir_y,new_name)
                movie_dir=os.path.join(dir_y,video)
                return movie_dir
        for F_f in os.listdir(dir_y):
            if os.path.isdir(os.path.join(dir_y,F_f)):
                movie_dir=search_movie(os.path.join(dir_y,F_f),movie_name.lower())
                if movie_dir is not None:
                    return movie_dir

    def setMovie():
        con_pre_mov=int(input("Wanna continue previous watched movie >> "))
        if con_pre_mov == 1:
            file=open('C:\\Users\\RAJAN\\Desktop\\Alexa.python.source\\playMovie.Data.txt','r')
            for line in file:
                movie_path=line
            file.close()
            return movie_path
        else:
            movie_path=search_movie("D:\Movies",input("( # for print all movies)\nEnter Movie name: ").lower())
            print('Directory: "{}"'.format(movie_path))
            if movie_path is None:
                print("INVALID MOVIE NAME ENTERED\n\t\tHere are the available MOVIES !!!\n.................................")
                movies_count=printMovies("D:\Movies",1)
                print("\n................................")
                print(" %d movies are available "%(movies_count))
                setMovie()
            else:
                #movie_path=movie_path.replace('\\','\\\\')
                return movie_path
    def write_file(typ,adress,message=True):
        if message:
            message=input("Type your message:\n\n\t\t")
        else:
            message=""
        if (not typ) or (not adress):
            open_type="None"
            open_adress="None"
        else:
            open_type=typ
            open_adress=adress
        connection=sqlite3.connect("ShutdownDB.db")
        cursor=connection.cursor()
        command=f"""INSERT INTO SHUTDOWN(MESSAGE,OPEN_TYPE,OPEN_ADRESS,POWER) VALUES ("{message}","{open_type}","{open_adress}","OFF");"""
        cursor.execute(command)
        connection.commit()
        connection.close()
    def shutdown():
        subprocess.Popen([power_off],shell=True)
        threading.Thread(target=os.system,args=('shutdown /t 10 /s /c " "',)).start()
        countdown()
    def record_shutdown(set):
        if check(set,"yes","y","sure","yea","yeah","si"):
            list=['Python','Movie','Series']
            for i in range(len(list)):
                print(" %d) %s"%(i+1,list[i]))
            cmd=input("\nWhich one >> ").lower()
            if check(cmd,"python","py"):
                i=0
                py_file_name_list=[]
                py_file_dir_list=[]
                for file in os.listdir("C:\\Users\\RAJAN\\Desktop"):
                    if file.endswith(".source"):
                        print(f'\n{file}: ')
                        for file2 in os.listdir(os.path.join("C:\\Users\\RAJAN\\Desktop",file)):
                            if file2.endswith(".py") or file2.endswith(".pyw"):
                                i+=1
                                py_file_name_list.append(file2)
                                py_file_dir_list.append(os.path.join("C:\\Users\\RAJAN\\Desktop",file,file2))
                                print("   %d) %s"%(i,file2))
                file_name=input("\nEnter the python file name >>")
                if file_name in py_file_name_list:
                    for i in range(len(py_file_name_list)):
                        if py_file_name_list[i]==file_name:
                            file_dir=py_file_dir_list[i]
                    write_file('python',file_dir)
                    next_due=1
                else:
                    speak("Invalid File Name")
                    write_file(None,None)
            elif check(cmd,"movie"):
                write_file('movie',setMovie())
            elif check(cmd,"series"):
                choice=input("\nContinueing series or Next episode ?  \n> ")
                if check(choice,"continue"):
                    write_file('series','continue')
                elif check(choice,"next"):
                    write_file('series','next')
                else:
                    write_file(None,None)
            else:
                write_file(None,None)
            shutdown()
        elif check(set,"cancel","abort","don"):
            speak("Shutdown Cancelled")
            sys.exit()
            os.system("exit")
        elif check(set,"no","na"):
            write_file(None,None,message=False)
            shutdown()
        else:
            record_shutdown(input(">"))
    record_shutdown(set)

except KeyboardInterrupt:
    speak("Shutdown Cancelled")
