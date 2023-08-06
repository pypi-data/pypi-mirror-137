# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 19:56:07 2018

@author: 10091
"""

from datetime import datetime,time,date
import time as ti
import os
import tkinter as tk

from chdf import *
import 登入 

def main():
    tmNow = datetime.now()
    d = datetime.today()

    chd('c:\\kencode\\down')
    with open('b.txt') as e:
        e = e.read().split()
    def sd():
        a = tk.Tk()
        a1 = tk.Label(a,text='要關機了，趕快儲存一下！')
        a1.pack()
        os.system('shutdown -s -f -t 60') 
        a.mainloop() 
    def shutdown():
        while True:
            with open('b.txt') as e:
                e = e.read().split()
            try:
                e[0] = e[0].split('/')
                e[1] = e[1].split('/')    
                tmNow = ti.strftime("%H:%M:%S").split(':')
                if int(tmNow[0])>=int(e[0][0]):
                    if int(tmNow[0])==int(e[0][0]):
                        if int(tmNow[1]) > int(e[0][1]):
                            sd()
                    else:
                        sd()
                elif int(tmNow[0])<=int(e[1][0]):
                    if int(tmNow[0])==int(e[1][0]):
                        if int(tmNow[1]) < int(e[1][1]):
                            sd()
                    else:
                        sd()
            except:
                pass
    shutdown()
if __name__ == '__main__':
    main()


