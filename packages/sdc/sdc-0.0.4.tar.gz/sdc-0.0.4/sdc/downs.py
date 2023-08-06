import tkinter as tk  
import time

from chdf import *
import 登入 

class Clock():
    def __init__(self):
        chd('./down')
        self.root = tk.Tk()
        self.root.title('自動關機')
        self.root.geometry(f'300x100+{self.root.winfo_screenwidth()-310}+0')
        self.label = tk.Label(text="", font=('Helvetica', 48), fg='red')
        self.label.pack()
        mybutton = tk.Button(self.root, text='設定',command=登入.smain,width=40,height=1,bg='red')
        mybutton.pack()
        self.update_clock()
        self.root.mainloop()
    
    def update_clock(self):
        y = time.strftime("%H:%M:%S").split(':')
        self.x = []
        try:
            with open('b.txt') as z:
                z = z.read().split()
            self.z = z
            self.z[0] = z[0].split('/')
            self.z[1] = z[1].split('/')
            for i in range(3):
                w = str(int(self.z[0][i])-int(y[i]))
                self.x.append(w)
            # print(self.x)
            for i in range(len(self.x)-1,-1,-1):
                if eval(self.x[i]) < 0 and i != 0:
                    self.x[i] = str(int(self.x[i])+60)
                    self.x[i-1] = str(int(self.x[i-1])-1)
            now = ':'.join(self.x)
            self.label.configure(text=now)
        except:
            pass
        self.root.after(1000, self.update_clock)
if __name__ == '__main__':
    a = Clock()