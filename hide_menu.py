# import matplotlib
# import matplotlib.pyplot as plt
# backend = matplotlib.get_backend()
# print(backend)

import tkinter as tk
import win32api,win32con
from tkinter import messagebox        #引入弹窗库
from threading import Thread

screen_x = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)   #获得屏幕分辨率X轴
screen_y = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)   #获得屏幕分辨率Y轴
cursor_width = 127
root = tk.Tk()
root.title("定位工具")
root.resizable(width=False, height=False) # 设置窗口是否可以变化长/宽，False不可变，True可变，默认为True
root.overrideredirect(True)
#root.attributes("-alpha", 0.3)窗口透明度70 %
root.attributes("-alpha", 0.7)#窗口透明度30 %
# root.geometry("300x200+10+10")
root.geometry(str(screen_x)+"x"+str(screen_y))
# root.geometry(str(screen_x)+"x"+str(screen_y)+"+50+50")
frame = tk.Frame(root, bg="blue",cursor="crosshair")
# frame.pack()
frame.configure(width = screen_x)
frame.configure(height = screen_y)
# frame.place(x=0, y=100)
frame.pack()
canvas = tk.Canvas(frame)

canvas.configure(width = screen_x)
canvas.configure(height = screen_y-100)
# canvas.configure(bg = "yellow")
canvas.configure(highlightthickness = 0)
canvas.configure(cursor="crosshair")
columnFont = ('微软雅黑', 18)
canvas.create_text(screen_x/2,30, text="设定pygame弹窗左上角的默认出现位置", font=columnFont, fill="black", justify=tk.CENTER)
close_clock = False

def on_closing():
    global close_clock
    close_clock = True
    global root
    global canvas
    global only_pos
    if only_pos:
        print("delete only_pos")
        canvas.delete(only_pos)
    if root:
        root.destroy()
        root = None
    close_clock = False

# root.protocol("WM_DELETE_WINDOW", on_closing)

cancel_png = tk.PhotoImage(file=r"res\cancel.png")
button_width = 86
button_height = 42
cancel_btn = tk.Button(frame, image=cancel_png, bg="#fdfdbc",activebackground="#fdfdbc",  bd=0, cursor="hand2",compound = tk.CENTER,command=on_closing, width=button_width, height=button_height)
cancel_btn.place(x=screen_x-100, y = 0)

# 显示文字
# canvas.create_text((700, 100), text="您可以在屏幕上点击您想要pygame窗口出现的位置!", font=("微软雅黑", 18))
# canvas.place(x=0, y=-100)


canvas.pack()
pos_gif = tk.PhotoImage(file=r"res\cursor.png")
marked_jpg = tk.PhotoImage(file=r"res\marked.png")

only_pos = None
only_mark = None

def locate(event):
    print(event.x, event.y)
    # print(event.type)
    # print(event.widget)
    # print(type(event.widget))
    if isinstance(event.widget, tk.Canvas):
        offset = cursor_width / 2
        global canvas
        global only_mark
        global only_pos
        if only_pos:
            canvas.delete(only_pos)
            only_pos = None
        # if event.x >= (screen_x-100) and event.x <= (screen_x-100+button_width) and event.y >= 0 and event.y <= button_height:
        #     print("点击了取消按钮")
        #     on_closing()
        #     return

        if only_mark:
            canvas.delete(only_mark)
            only_mark = None
        only_pos = canvas.create_image(event.x+offset, event.y+offset, image=pos_gif)  #这看上去是一个瞬间的操作，我们得加一个阻塞的事件
        only_mark = canvas.create_image(event.x+offset, event.y+200, image=marked_jpg)  #这看上去是一个瞬间的操作，我们得加一个阻塞的事件
        Thread(target=delete_mark, daemon=True).start()
        global close_clock
        if not close_clock:
        # only_mark = None
            print("not close_clock")
            tk.mainloop()
        print("点击canvas")
    elif isinstance(event.widget, tk.Button):
        print("点击button")
        on_closing()

    # show_click_pos(frame, event.x, event.y)
    # res = messagebox.askokcancel(title='定位确认',message='您是否确认定位在这里？')
    # if res == True:
    #     #Todo: 这里应该有一个在刚才点击位置
    #     pass
    #     global root
    #     if root:
    #         root.destroy()
    #         root = None
    # print(res)  

def delete_mark():
    global canvas
    global only_mark
    import time
    enter_name = time.time()
    while only_mark:
        cur_time = time.time()
        if cur_time - enter_name > 2:
            canvas.delete(only_mark)
            only_mark = None
            break
        time.sleep(0.1)
    

root.bind("<Button-1>",locate)
# root.bind("<ButtonRelease-1>",locate)

def move(event):
    global x,y
    new_x = (event.x-x)+root.winfo_x()
    new_y = (event.y-y)+root.winfo_y()
    s = "300x200+" + str(new_x)+"+" + str(new_y)
    root.geometry(s)
    print("s = ",s)
    print(root.winfo_x(),root.winfo_y())
    print(event.x,event.y)
def button_1(event):
    global x,y
    x,y = event.x,event.y
    print("event.x, event.y = ",event.x,event.y)
    canvas.bind("<B1-Motion>",move)
    canvas.bind("<Button-1>",button_1)


root.mainloop()

#自己加个双击鼠标事件 关闭窗口 不然结束程序很不爽 要关闭IDE 