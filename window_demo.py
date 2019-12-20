import tkinter as tk
import time
import pygame
from pygame.locals import *
from threading import Thread
import win32api,win32con
from tkinter import messagebox        #引入弹窗库

screen_x = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)   #获得屏幕分辨率X轴
screen_y = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)   #获得屏幕分辨率Y轴


def on_closing():
    global moni_window
    if moni_window:
        moni_window.destroy()
        moni_window = None

moni_window = tk.Tk()                   #只有一个Tk窗口
# moni_window = tk.Toplevel()           #已有Tk窗口使用Toplevel
moni_window.title('弹窗位置设定工具')
# moni_window.geometry("324x300")
moni_window.geometry(str(screen_x)+"x"+str(screen_y))
moni_window.protocol('WM_DELETE_WINDOW',on_closing)
moni_window.attributes("-alpha", 0.6)
#设置窗口大小不可改变
moni_window.resizable(False, False)

def callback():
    tk_label_y = 30
    # 注意设置坐标的时候是换算后的
    # rate = get_rate()  # 获取缩放比例
    # x = int(moni_window.winfo_x()/rate)
    # y = int((moni_window.winfo_y()+tk_label_y)/rate)
    # set_win_location(x,y)
    global moni_window
    if moni_window:
        moni_window.destroy()
        moni_window = None


# x,y = get_win_location()

# if x is not None and y is not None:
#     rate = get_rate()  # 获取缩放比例
#     x = int(x*rate)
#     y = int(y*rate)
#     moni_window.geometry("+"+str(x)+"+"+str(y))

# moni_background = tk.PhotoImage(file="moni_bg.png")
frame = tk.Frame(moni_window, bg="yellow",cursor="crosshair")
frame.pack()
# tip_text = "如果你想设定pygame弹窗位置\n可以拖动这个窗口，并点击确认\n如果无需调整，可点击取消"
# text=tip_text,
moni_background = tk.PhotoImage(file=r"res\moni_bg_test.png")
ok_png = tk.PhotoImage(file=r"res\ok.png")
cancel_png = tk.PhotoImage(file=r"res\cancel.png")
flower_jpg = tk.PhotoImage(file=r"res\flower.jpg")
pos_png = tk.PhotoImage(file=r"res\pos.gif")
cursor_png = tk.PhotoImage(file=r"res\cursor.png")

tip_label = tk.Label(frame,image=flower_jpg,compound = tk.CENTER,font=("Microsoft YaHei",13),fg='black', justify="left", width=screen_x, height=screen_y, wraplength=300)
tip_label.pack()



# ok_png = tk.PhotoImage(file="ok.png")
# ok_btn = tk.Button(frame, image=ok_png, bg="#fdfdbc", activebackground="#fdfdbc", bd=0, cursor="hand2", compound = tk.CENTER,command=callback, width=86, height=42)
# ok_btn.place(relx=0.2, rely=0.7)    #注意为了保持按钮的对称，ok_btn和cancel_btn的relx之和必须为0.735， ok_btn的relx小于0.23


# cancel_btn = tk.Button(frame, image=cancel_png, bg="#fdfdbc",activebackground="#fdfdbc",  bd=0, cursor="hand2",compound = tk.CENTER,command=on_closing, width=86, height=42)
# cancel_btn.place(relx=0.535, rely=0.7)

x = 0
y = 0
def locate(event):
    print(event.x)
    print(event.y)
    global frame
    show_click_pos(frame, event.x, event.y)
    res = messagebox.askokcancel(title='定位确认',message='您是否确认定位在这里？')
    if res == True:
        #Todo: 这里应该有一个在刚才点击位置
        pass
        global moni_window
        if moni_window:
            moni_window.destroy()
            moni_window = None
    print(res)  # return ok)
#     print(event.x,event.y)
#     global moni_window
#     global x
#     global y
#     x,y = event.x, event.y
#     moni_window.geometry("324x300"+"+"+str(x)+"+"+str(y))
    # if event.type==pygame.MOUSEMOTION:
    #     x, y = event.pos  直接获取鼠标的坐标
#     pygame.mouse.set_visible(False)

       

moni_window.bind("<Button-1>",locate)
# moni_window.attributes("-fullscreen", True)

def show_click_pos(frame, x, y):
#     pos_label = tk.Label(frame,image=pos_png,compound = tk.CENTER,font=("Microsoft YaHei",13),fg='black',justify="left", wraplength=300)
#     pos_label.pack()
    # import matplotlib
    # from matplotlib import pyplot as plt
    # from PIL import Image
    # img = Image.open("pos.jpg")
    # fig = plt.figure()
    
    # fig.canvas.manager.window.wm_geometry("+"+str(x)+"+"+str(y))
    # fig.imshow(img)
    # fig.figimage(img)
    # plt.show()
    # fig.show()

    print("show_click_pos finish")

def get_full_pos():
    import pyautogui
    try:
        while True:
            x, y = pyautogui.position()
            x -= 100
            y -= 100
            # global moni_window
            # moni_window.geometry("324x300"+"+"+str(x)+"+"+str(y))
            # print(x,y)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print('\nExit.')

Thread(target=get_full_pos, daemon=True).start()
moni_window.mainloop()
