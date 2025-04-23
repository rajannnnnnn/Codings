import subprocess
import pyautogui as do
import time
import sys
import sqlite3
import os
not_printed=True
def printSeries(MY_DIR=r"D:\WebSeries"):
    global series_list
    series_list=[]
    for index,series in enumerate(os.listdir(MY_DIR)):
        print(f"{index+1} ) {series}")
        series_list.append(series)
def main(key="continue"):
    MY_DIR=r"D:\WebSeries"
    connection=sqlite3.connect("series.db")
    cursor=connection.cursor()
    fetchall=cursor.execute(f"""SELECT * FROM SERIES""")
    data=fetchall.fetchall()
    id,name,season,episode=data[len(data)-1]
    if "continue" in key:                                                #####continue
        path=os.path.join(MY_DIR,name,f"Season {season}")
        path=os.path.join(path,os.listdir(path)[episode-1])
    elif "next" in key:                                                     #########next
        path=os.path.join(MY_DIR,name)
        seasons=os.listdir(path)
        season_length=len(seasons)
        temp_path=os.path.join(path,f"Season {season}")
        episode_length=len(os.listdir(temp_path))
        if episode_length==episode:
            if season_length==season:
                print(f"Couldnot go to the next episode\nYou have completed '{name}'")
            else:
                print(f"You completed Season {season}")
                season+=1
                episode=1
                path=os.path.join(path,f"Season {season}")
                path=os.path.join(path,os.listdir(path)[episode-1])
        else:
            path=os.path.join(path,f"Season {season}")
            episode+=1
            path=os.path.join(path,os.listdir(path)[episode])
    elif "select" in key:                                                   ##########select
        global not_printed
        if not_printed:
            printSeries()
            print()
            not_printed=False
        name=input("Series name: ").lower()
        found=False
        for original_name in series_list:
            if original_name.lower()==name:
                name=original_name
                found=True
                break
        if not found:
            print("Invalid name")
            main("select")
            return
        path=os.path.join(MY_DIR,name)
        season=int(input("Season: "))
        season_length=len(os.listdir(path))
        if season<=season_length:
            path=os.path.join(path,f"Season {season}")
        else:
            print(f"Season {season} is not available")
            main("select")
            return
        episode=int(input("Episode: "))
        episode_length=len(os.listdir(path))
        if episode<=episode_length:
            path=os.path.join(path,os.listdir(path)[episode-1])
        else:
            print(f"Episode {episode} is not available")
            main("select")
            return
    print(path)
    subprocess.Popen([r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe",path],shell=True)
    command=f"""INSERT INTO SERIES(NAME,SEASON,EPISODE) VALUES("{name}","{season}","{episode}");"""
    cursor.execute(command)
    connection.commit()
    connection.close()
    return name,season,episode
if __name__=="__main__":
    main(input("Playing type: "))
