# import matplotlib
# import matplotlib.pyplot as plt
# backend = matplotlib.get_backend()
# print(backend)

import tkinter
import win32api,win32con
from tkinter import messagebox        #引入弹窗库
from threading import Thread

screen_x = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)   #获得屏幕分辨率X轴
screen_y = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)   #获得屏幕分辨率Y轴
cursor_width = 127
root = tkinter.Tk()
root.title("您可以在屏幕上点击您想要pygame窗口出现的位置!")
root.resizable(width=False, height=False) # 设置窗口是否可以变化长/宽，False不可变，True可变，默认为True
# root.overrideredirect(True)
#root.attributes("-alpha", 0.3)窗口透明度70 %
root.attributes("-alpha", 0.7)#窗口透明度60 %
# root.geometry("300x200+10+10")
root.geometry(str(screen_x)+"x"+str(screen_y))
# root.geometry(str(screen_x)+"x"+str(screen_y)+"+50+50")
frame = tkinter.Frame(root, bg="blue",cursor="crosshair")
# frame.pack()
frame.configure(width = screen_x)
frame.configure(height = screen_y)
# frame.place(x=0, y=100)
frame.pack()
canvas = tkinter.Canvas(frame)

canvas.configure(width = screen_x)
canvas.configure(height = screen_y-100)
# canvas.configure(bg = "yellow")
canvas.configure(highlightthickness = 0)
canvas.configure(cursor="crosshair")
# 显示文字
# canvas.create_text((700, 100), text="您可以在屏幕上点击您想要pygame窗口出现的位置!", font=("微软雅黑", 18))
# canvas.place(x=0, y=-100)


canvas.pack()
x, y = 0, 0

def locate(event):
    print(event.x, event.y)
    pos_gif = tkinter.PhotoImage(file=r"res\cursor.png")
    marked_jpg = tkinter.PhotoImage(file=r"res\marked.png")
    offset = cursor_width / 2
    global canvas
    canvas.create_image(event.x+offset, event.y+offset, image=pos_gif)  #这看上去是一个瞬间的操作，我们得加一个阻塞的事件
    mark = canvas.create_image(event.x+offset, event.y+200, image=marked_jpg)  #这看上去是一个瞬间的操作，我们得加一个阻塞的事件
    Thread(target=delete_mark, args=[mark]).start()
    tkinter.mainloop()
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

def delete_mark(mark):
    global canvas
    import time
    time.sleep(3)
    canvas.delete(mark)
    

root.bind("<Button-1>",locate)
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