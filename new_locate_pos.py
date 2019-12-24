# import matplotlib
# import matplotlib.pyplot as plt
# backend = matplotlib.get_backend()
# print(backend)

import tkinter as tk
import win32api,win32con
from tkinter import messagebox        #引入弹窗库
from threading import Thread
import time

screen_x = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)   #获得屏幕分辨率X轴
screen_y = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)   #获得屏幕分辨率Y轴

class LocatePosTool():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("定位工具")
        self.root.resizable(width=False, height=False) # 设置窗口是否可以变化长/宽，False不可变，True可变，默认为True
        self.root.overrideredirect(True)
        self.root.attributes("-alpha", 0.7)#窗口透明度=1-x
        self.root.geometry(str(screen_x)+"x"+str(screen_y)) #后面可以加位置参数"+x+y" 
        self.root.bind("<Button-1>",self.locate)     #左键点击事件

        self.frame = tk.Frame(self.root, bg="blue",cursor="crosshair")
        self.frame.configure(width = screen_x)
        self.frame.configure(height = screen_y)
        # self.frame.place(x=0, y=100)
        self.frame.pack()

        self.canvas = tk.Canvas(self.frame)
        self.canvas.configure(width = screen_x)
        self.canvas.configure(height = screen_y-100)
        # self.canvas.configure(bg = "yellow")
        self.canvas.configure(highlightthickness = 0)
        self.canvas.configure(cursor="crosshair")

        # 显示文字
        columnFont = ('微软雅黑', 18)
        self.canvas.create_text(screen_x/2,30, text="设定pygame弹窗左上角的默认出现位置", font=columnFont, fill="black", justify=tk.CENTER)
        

        cancel_png = tk.PhotoImage(file=r"res\cancel.png")
        button_width = 86
        button_height = 42
        cancel_btn = tk.Button(self.frame, image=cancel_png, bg="#fdfdbc",activebackground="#fdfdbc",  bd=0, cursor="hand2",compound = tk.CENTER,command=self.on_closing, width=button_width, height=button_height)
        print("screen_x是", screen_x)
        cancel_btn.place(x=screen_x-100, y = 0)
 

        self.canvas.pack()

        self.only_pos = None
        self.only_mark = None

        self.root.mainloop()

        # self.root.protocol("WM_DELETE_WINDOW", on_closing)

    def on_closing(self):
        if self.only_pos:
            print("delete self.only_pos")
            self.canvas.delete(self.only_pos)
        if self.root:
            self.root.destroy()
            self.root = None
    
    
    def locate(self, event):
        print(event.x, event.y)
        cursor_width = 127
        if isinstance(event.widget, tk.Canvas):
            offset = cursor_width / 2
            if self.only_pos:
                self.canvas.delete(self.only_pos)
                self.only_pos = None

            if self.only_mark:
                self.canvas.delete(self.only_mark)
                self.only_mark = None
            pos_gif = tk.PhotoImage(file=r"res\cursor.png")
            marked_jpg = tk.PhotoImage(file=r"res\marked.png")
            self.only_pos = self.canvas.create_image(event.x+offset, event.y+offset, image=pos_gif)  
            self.only_mark = self.canvas.create_image(event.x+offset, event.y+200, image=marked_jpg)  #这看上去是一个瞬间的操作，我们得加一个阻塞的事件
            Thread(target=self.delete_mark, daemon=True).start()
            tk.mainloop()
            print("点击self.canvas")
        elif isinstance(event.widget, tk.Button):
            #点击了取消按钮
            print("点击button")
            self.on_closing()

    

    
    def delete_mark(self):
        enter_name = time.time()
        while self.only_mark:
            cur_time = time.time()
            if cur_time - enter_name > 2:
                self.canvas.delete(self.only_mark)
                self.only_mark = None
                break
            time.sleep(0.1)

test = LocatePosTool()


