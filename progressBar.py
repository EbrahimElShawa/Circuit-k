from tkinter import *
from tkinter.ttk import *


def update(new_percentage, cur_sec):
    bar['value'] = cur_sec
    percent.set(str(round(new_percentage, 2)) + "%")
    text.set(str(round(cur_sec, 5)) + "/" + str(mx) + " second completed")
    window.update_idletasks()
    if bar['value'] == mx:
        window.destroy()


def main(max):
    global window, percent, text, bar, mx, cur
    mx = max
    cur = 0
    window = Tk()
    window.title("Loading....")
    percent = StringVar()
    text = StringVar()

    bar = Progressbar(window, orient=HORIZONTAL, length=300, mode='determinate', maximum=max)
    bar.pack(pady=10)

    Label(window, textvariable=percent).pack()
    Label(window, textvariable=text).pack()

# Delay before focusing on another widget
