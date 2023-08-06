from random import randint, seed
from tkinter.ttk import Notebook
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk

from numpy import size

def setting():
    class Setting(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title("設定")   	 
            self.geometry("240x250+800+50")
            self.init_menubar()
            self.notebook = Notebook(self)
            self.notebook.pack(side = tk.TOP,fill=tk.BOTH, expand=tk.YES)
            self.init_notebookpage_1()
            self.init_notebookpage_2()

            
        def menu_1_command(self, event = None):
            print("menu_1")

        def init_menubar(self):
            menubar = tk.Menu(self)
            self.configure(menu=menubar)
            functions = tk.Menu(menubar)
            functions.add_command(label="menu1", command = self.menu_1_command)
            menubar.add_cascade(label="Functions", menu=functions)    
        def init_notebookpage_1(self):
            self.notebookpage_1_tab = tk.Frame(self.notebook)
            self.l10 = tk.Label(self.notebookpage_1_tab,text='from') # english L
            self.l10.pack(pady=5)
            self.hv = [i for i in range(1,24+1)]
            self.msv = [i for i in range(0,60+1)]
            self.c100 = ttk.Combobox(self.notebookpage_1_tab, values = self.hv,width=3,height=3) 
            self.c100.place(x=50,y=23)
            self.c101 = ttk.Combobox(self.notebookpage_1_tab, values = self.msv,width=3,height=3) 
            self.c101.place(x=100,y=23)
            self.c102 = ttk.Combobox(self.notebookpage_1_tab, values = self.msv,width=3,height=3) 
            self.c102.place(x=150,y=23)	
            self.l11 = tk.Label(self.notebookpage_1_tab,text='to') # english L
            self.l11.place(x=110,y=50)
            self.c110 = ttk.Combobox(self.notebookpage_1_tab, values = self.hv,width=3,height=3) 
            self.c110.place(x=50,y=70)
            self.c111 = ttk.Combobox(self.notebookpage_1_tab, values = self.msv,width=3,height=3) 
            self.c111.place(x=100,y=70)
            self.c112 = ttk.Combobox(self.notebookpage_1_tab, values = self.msv,width=3,height=3) 
            self.c112.place(x=150,y=70)	
            self.font0 = tkFont.Font(size=10)
            self.l12 = tk.Label(self.notebookpage_1_tab,text='(24小時制)',font=self.font0) # english L
            self.l12.place(x=90,y=100)
            self.notebook.add(self.notebookpage_1_tab, text=" 時間")
        def init_notebookpage_2(self):
            self.notebookpage_2_tab = tk.Frame(self.notebook)
            self.l20 = tk.Label(self.notebookpage_2_tab,text='帳號')
            self.l20.pack()
            self.e20 = tk.Entry(self.notebookpage_2_tab)
            self.e20.pack()
            self.l21 = tk.Label(self.notebookpage_2_tab,text='密碼(僅限數字)')
            self.l21.pack()
            self.e21 = tk.Entry(self.notebookpage_2_tab,show = '*')
            self.e21.pack()
            self.l22 = tk.Label(self.notebookpage_2_tab,text='確認密碼')
            self.l22.pack()
            self.e22 = tk.Entry(self.notebookpage_2_tab,show = '*')
            self.e22.pack()
            self.l23 = tk.Label(self.notebookpage_2_tab,text='(可選)問題&回答')
            self.l23.place(x=70,y=120)
            self.e23 = tk.Entry(self.notebookpage_2_tab,width=10)
            self.e23.place(x=43,y=140)
            self.font1 = tkFont.Font(size=10,weight="bold")
            self.l24 = tk.Label(self.notebookpage_2_tab,text=':',font=self.font1)
            self.l24.place(x=113,y=138)
            self.e24 = tk.Entry(self.notebookpage_2_tab,width=10)
            self.e24.place(x=123,y=140)
            self.notebook.add(self.notebookpage_2_tab, text="新帳密")
    def c():
        ba1 = a.e21.get()
        ba2 = a.e22.get()
        e = []
        e.append(ba1)
        e.append(ba2)
        h = 0
        l = 0
        if not ((ba1 and ba2) or ((not ba1) and (not ba2))):
            h = 1
            l+=1
        if h == 0:
            if ba1 == ba2:
                l += 1
            else:
                a1 = tk.Tk()
                a1.geometry('+850+150')
                a11 = tk.Label(a1,text='密碼不一樣')
                a11.pack()
                a1.mainloop() 
        ba3 = a.e23.get()
        ba4 = a.e24.get()
        h = 0
        if (ba3 and ba4) or ((not ba3) and (not ba4)):
            l+=1
        else:
            a2 = tk.Tk()
            a2.geometry('+850+150')
            a21 = tk.Label(a2,text='問題和答案必須都有或都沒有')
            a21.pack()
            a2.mainloop() 

        if l == 2:
            a.quit()
        
    a = Setting()
    b = tk.Button(a,command=c,text='確定')
    b.pack()
    a.mainloop()
    d = [a.c100.get(),a.c101.get(),a.c102.get(),a.c110.get(),a.c111.get(),a.c112.get()]
    e = [a.e20.get(),a.e21.get()]
    h = 0
    for i in d:
        if not i:
            h = 1
            break
    if h == 0:
        with open('..\\down\\b.txt','w') as l:
            print(f'{d[0]}/{d[1]}/{d[2]} {d[3]}/{d[4]}/{d[5]}')
            l.write(f'{d[0]}/{d[1]}/{d[2]} {d[3]}/{d[4]}/{d[5]}')  
    h = 0  
    for i in e:
        if not i:
            h = 1
            break
    if h == 0:    
        seed(int(e[1]))
        m = ''
        for i in range(len(e[0])):
            b = randint(1,10)
            seed(randint(b,100)**randint(1,b))
            m += str(ord(e[0][i])+b)
        with open('..\\down\\a.txt','w') as n:
            print(m)
            n.write(m) 
    if a.e23.get():
        with open('..\\down\\c.txt','w') as cc:
            cc.write(f'{a.e23.get()} {a.e24.get()}')
if __name__ == '__main__':
    setting()