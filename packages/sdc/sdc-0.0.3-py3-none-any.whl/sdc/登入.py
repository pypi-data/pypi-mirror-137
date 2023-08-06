from random import randint, seed
from time import sleep
from tkinter import Button, Entry, Tk
import tkinter as tk

import chdf,setting

class SChm():
    def go(self,text='登入'):
        self.text = text
        self.root = Tk()
        self.root.geometry('100x100+800+100')
        self.e0 = Entry(self.root,width=25)
        self.e0.pack(pady=5,padx=5)
        self.e1 = Entry(self.root,show='*',width=25)
        self.e1.pack(pady=5,padx=5)
        self.b0 = Button(self.root,command=self.a,text=self.text)
        if text == '登入':
            self.b0.place(x=10,y=60)
            self.b1 = Button(self.root,command=self.b,text='救援')
            self.b1.place(x=70,y=60) 
        else:
            self.b0.pack(pady=5,padx=5)
        self.root.mainloop()
    def a(self):
        a = self.e0.get()
        d = int(self.e1.get())
        seed(d)
        c = ''
        for i in range(len(a)):
            b = randint(1,10)
            seed(randint(b,100)**randint(1,b))
            c += str(ord(a[i])+b)
        self.root.quit()
        self.c = c        
    def b(self):
        with open('..\\down\\c.txt') as c:
            c = c.read().split()
        with open('..\\down\\a.txt') as a:
            a = a.read()
        a1 = tk.Tk()
        a1.geometry('+850+150')
        a11 = tk.Label(a1,text=f'{c[0]}')
        a11.pack()
        a12 = tk.Entry(a1)
        a12.pack()
        def aa():
            if a12.get() == c[1]:
                self.c = a
                self.root.quit()
        a13 = tk.Button(a1,text = '確定',command=aa)
        a13.pack()
        a1.mainloop() 

def smain():
    chdf.chd('../down')
    a = chdf.chff('a.txt')
    if a == '0':
        b = SChm()
        b.go('新密碼')
        b = b.c
        print(b)
        c = open('a.txt','w')
        c.write(b)
        c.close()
    else:
        b = SChm()
        b.go()
        b = b.c
        if a == b:
            setting.setting()
            








# 非視窗
def chm():
    a=input()
    d = int(input())
    seed(d)
    c = ''
    for i in range(len(a)):
        b = randint(1,10)
        seed(randint(b,100)**randint(1,b))
        c += str(ord(a[i])+b)
    return c
def main():
    chdf.chd('../down')
    a = chdf.chff('a.txt')
    if a == '0':
        b = chm()
        print(b)
        c = open('a.txt','w')
        c.write(b)
        c.close()
    else:
        b = chm()
        if a == b:
            a = input('1.改密碼 2.設時間 : ')
            if a == '1':
                b = chm()
                print(b)
                c = open('a.txt','w')
                c.write(b)
                c.close()
            elif a == '2':
                print('不能使用的時間')
                c = input('從 hh/mm/ss : ')
                d = input('到 hh/mm/ss : ')
                with open('b.txt','w') as b:
                    b.write(c)
                    b.write(' '+d)

if __name__ == '__main__':
    main()