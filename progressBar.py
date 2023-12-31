from tkinter import *
from tkinter.ttk import *

def updtae(new_percantage, cur_sec):
    bar['value'] = cur_sec
    percent.set(str(round(new_percantage,2)) + "%")
    text.set(str(round(cur_sec,5)) + "/" + str(mx) + " second completed")
    window.update_idletasks()


def main(max):
    global window, percent, text, bar, mx , cur
    mx = max
    cur = 0
    window = Tk()

    percent = StringVar()
    text = StringVar()

    bar = Progressbar(window, orient=HORIZONTAL, length=300, mode='determinate', maximum=max)
    bar.pack(pady=10)

    percentLabel = Label(window, textvariable=percent).pack()
    taskLabel = Label(window, textvariable=text).pack()


# Delay before focusing on another widget
