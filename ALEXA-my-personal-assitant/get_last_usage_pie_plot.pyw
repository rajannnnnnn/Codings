import matplotlib.pyplot as plt
import pandas as pd
import apps_tracer
import threading
import os
import subprocess
class PieShowUsage:
    def __init__(self,csv_file):
        self.csv_file=csv_file
        self.file = pd.read_csv(self.csv_file)
        self.group=self.file.groupby("Application")
        self.application=[]
        self.runtime=[]
        self.percent=[]
        self.app_runtime=[]
        self.app_name=[]
        self.app_runtime_hours=[]
        self.negleted_app_name=[]
        self.negleted_app_runtime=[]
        self.negleted_app_runtime_hours=[]
        self.labels=[]
    def showPie(self,neglet_percent_below=10):
        self.low_percent=neglet_percent_below
        for name,timing in self.group:  
            self.application.append(name)
            self.runtime.append(int(len(timing)))
        __summ=sum(self.runtime)
        for unit in self.runtime:
            per=round((unit/__summ)*100,2)
            self.percent.append(per)
        for index,value in enumerate(self.percent):
            if value>=self.low_percent:
                self.app_name.append(self.application[index])
                self.app_runtime.append(value)
                self.app_runtime_hours.append(self.runtime[index])
            else:
                self.negleted_app_name.append(self.application[index])
                self.negleted_app_runtime.append(value)
                self.negleted_app_runtime_hours.append(self.runtime[index])
        for index,value in enumerate(self.app_runtime_hours):
            minutes=value/60
            self.app_runtime_hours[index]=minutes
        print(f"{self.app_name}\n{self.app_runtime}\n{self.app_runtime_hours}\n\n{self.negleted_app_name}\n{self.negleted_app_runtime}\n{sum(self.negleted_app_runtime)}\n\nTotal={sum([sum(self.negleted_app_runtime),sum(self.app_runtime)])}")
        plt.pie(self.app_runtime_hours,labels=self.app_name)#self.labels)
        plt.show()
if __name__=="__main__":
    show=PieShowUsage(r"C:\Users\RAJAN\Desktop\Alexa.python.source\running_usage.csv")
    subprocess.Popen([r"C:\Users\RAJAN\Desktop\Alexa.python.source\apps_tracer.pyw"],shell=True)
    show.showPie(5)
