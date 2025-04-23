from moviepy.editor import VideoFileClip
import random
import os
import subprocess
import re
path = r"D:\Movies"
movies = {}
movies_count = sum(1 for file in os.listdir(path) if file.lower().endswith(('.mp4', '.avi', '.mkv', '.mov', '.flv', '.wmv', '.webm')))
def store_directory(directory):
    with open('directory_store.txt', 'w') as file:
        file.write(directory)
def fetch_directory():
    try:
        with open('directory_store.txt', 'r') as file:
            content = file.read().strip()
            if not content:
                return None
            return content
    except FileNotFoundError:
        return None
def clean_string(input_string):
    return re.sub(r'\s+', ' ', input_string).strip()
def fetch_movies(min_=(0,0),max_=False):
    movies.clear()
    if max_ is not False:
        min_ = int((int(min_[0])*60)+int(min_[1]))
        max_ = int((int(max_[0])*60)+int(max_[1]))
        for name in os.listdir(path):
            for genre in clean_string(name[:-4]).split(" "):
                minutes = VideoFileClip(os.path.join(path,name)).duration/60
                if round(minutes)>int(min_) and round(minutes)<int(max_):
                    try:
                        movies[genre].append(name)
                    except KeyError:
                        movies[genre] = [name]
    if max_ is False:
        for name in os.listdir(path):
            for genre in name[:-4].split(" "):
                minutes = VideoFileClip(os.path.join(path,name)).duration/60
                try:
                    movies[genre].append(name)
                except KeyError:
                    movies[genre] = [name]
def play(name):
    store_directory(os.path.join(path,name))
    subprocess.Popen([r"C:\Program Files\VideoLAN\VLC\vlc.exe", os.path.join(path,name)])
def by_genre(typ = "by genre"):
    if typ == "by genre":
        fetch_movies()
    print("Choose one and type on the prompt: ")
    for genre in movies.keys():
        print(" ",genre)
    inp = input(">>>")
    if typ == "by runtime":
        if inp in movies.keys():
            play(random.choice(movies[inp]))
        else:
            play(random.choice(movies[random.choice(movies.keys())]))
        return
    if inp in movies.keys():
        if len(movies[inp]) == 1:
            play(movies[inp][0])
        else:
            for index,movie in enumerate(movies[inp]):
                minutes = VideoFileClip(os.path.join(path,movie)).duration/60
                print(index+1,")",str(round(minutes/60))+":"+str(round(minutes%60)))
            try:
                play(movies[inp][int(input(">>>"))-1])
            except ValueError:
                play(random.choice(movies[inp]))
    else:
        start()
def by_runtime():
    min_ = tuple(input("Min runtime: ").split())
    max_ = tuple(input("Max runtime: ").split())
    if len(min_) == 2 and len(max_) == 2:
        fetch_movies(min_,max_)
    by_genre("by runtime")
    minutes = VideoFileClip(os.path.join(path,movie)).duration/60
    print(index+1,")",str(round(minutes/60))+":"+str(round(minutes%60)))
    
    
def start():
    print("----------------------------------------------------------------------------------------")
    print("                                   WATCH MOVIES NOW")
    print("                 Cinema is not only an Entertainment, also an experience")
    print("                                                                              - Rajan N")
    print("----------------------------------------------------------------------------------------")
    print(f" Movies count: {movies_count}")
    print()
    print(" 1) Specific Genre in mind ?\n 2) Wanna go with specific runtime ?")
    file = fetch_directory()
    if file is not None:
        print(f""" 3) Continue your last cinema which is "{os.path.basename(file)[:-4]}" """)
        print(f""" 4) Delete your last cinema which is "{os.path.basename(file)[:-4]}" """)
    inp = int(input(" >>> "))
    if inp == 1:
        by_genre()
    elif inp == 2:
        by_runtime()
    elif file is not None:
        if inp == 3:
            play(os.path.basename(file))
        elif inp == 4:
            os.remove(file)
            print(f"os.remove {file}")
            with open('directory_store.txt', 'w') as file:
                pass
    else:
        print("\n\n\n")
        start()
if __name__ == "__main__":
    start()
