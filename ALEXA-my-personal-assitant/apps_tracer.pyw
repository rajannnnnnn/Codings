import win32gui
import time
import csv
def startTracing():
    with open(r"C:\Users\RAJAN\Desktop\Alexa.python.source\all_usage.csv","a") as all_data_file:
        with open(r"C:\Users\RAJAN\Desktop\Alexa.python.source\running_usage.csv","r") as current_file:
            for index,data in enumerate(current_file.readlines()):
                if index!=0:
                    all_data_file.write(data)
    with open("running_usage.csv","w") as csv_file:
        writer=csv.writer(csv_file)
        writer.writerow(["Application","Time"])
    while True:
        name = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        app_data=[name.replace("*",""),1]
        with open("running_usage.csv","a") as csv_file:
            writer=csv.writer(csv_file)
            writer.writerow(app_data)
        time.sleep(1)
if __name__=="__main__":
    startTracing()
