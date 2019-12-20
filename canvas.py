import tkinter as tk

win = tk.Tk()
# win.geometry("600x400+200+100")
win.geometry("600x400")

# 创建画布
canvas = tk.Canvas(win, bg="orange")
canvas.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

win.mainloop()