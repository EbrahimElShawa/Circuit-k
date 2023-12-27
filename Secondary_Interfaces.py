import tkinter as tk
from tkinter import ttk

ASSETS_PATH = "P:\\Study\\Python\\Tick_2\\assets"
font = ('Times New Roman', 10, 'bold')
magnitude, angle, frequency, ramp_time, equation = None, None, None, None, None


def set_values_window(window, component_name):
    global ASSETS_PATH, magnitude, angle, frequency, ramp_time, equation
    if component_name == 'AC':

        frame1_path = ASSETS_PATH + "\\frame1\\"
        values_window = tk.Toplevel(window)
        values_window.title("Set Value")
        values_window.geometry("300x128")
        values_window.iconbitmap(frame1_path + "AC_Power.ico")
        canvas = tk.Canvas(values_window, bg="#FFFFFF", height=150, width=300, bd=0)
        canvas.place(x=0, y=0)

        image_1 = tk.PhotoImage(file=frame1_path + "image_1.png")
        image_2 = tk.PhotoImage(file=frame1_path + "image_2.png")
        image_3 = tk.PhotoImage(file=frame1_path + "image_3.png")
        image_4 = tk.PhotoImage(file=frame1_path + "image_4.png")
        add_element_button_image = tk.PhotoImage(file=frame1_path + "button_1.png")
        add_element_button = tk.Button(values_window, image=add_element_button_image, borderwidth=0,
                                       command=lambda: add_element(component_name))
        combobox_value = tk.StringVar()
        wave_type_combobox = ttk.Combobox(values_window, textvariable=combobox_value, state='readonly',
                                          values=['SINE', 'RECTANGLE', 'TRIANGLE', 'SAWTOOTH'])
        mag_entry = tk.Entry(values_window, bg="#D9D9D9", foreground="#780000", font=font)
        ang_entry = tk.Entry(values_window, bg="#D9D9D9", foreground="#780000", font=font)
        freq_entry = tk.Entry(values_window, bg="#D9D9D9", foreground="#780000", font=font)
        ramp_entry = tk.Entry(values_window, bg="#D9D9D9", foreground="#780000", font=font)
        eq_entry = tk.Entry(values_window, bg="#D9D9D9", foreground="#780000", font=font)

        canvas.create_image(36, 17, image=image_1)
        canvas.create_image(188, 17, image=image_2)
        canvas.create_image(36.0, 113, image=image_3)
        canvas.create_image(19.0, 80.0, image=image_4)
        add_element_button.place(x=210, y=106, width=82, height=15)
        wave_type_combobox.place(x=210, y=78, width=80, height=20)
        mag_entry.place(x=8, y=35, width=52, height=18)
        ang_entry.place(x=85, y=35, width=32, height=18)
        freq_entry.place(x=148, y=35, width=30, height=18)
        ramp_entry.place(x=220, y=35, width=30, height=18)
        eq_entry.place(x=80, y=106, width=105, height=15)

        magnitude, angle, frequency = mag_entry.get(), ang_entry.get(), freq_entry.get()
        ramp_time, equation = ramp_entry.get(), eq_entry.get()

        values_window.resizable(False, False)
        values_window.mainloop()

    else:
        frame2_path = ASSETS_PATH + "\\frame2\\"
        values_window = tk.Toplevel(window)
        values_window.geometry("230x100")
        values_window.title("Set Value")
        values_window.iconbitmap(frame2_path + "DC.ico")
        canvas = tk.Canvas(values_window, bg="#FFFFFF", height=100, width=230, bd=0)
        canvas.place(x=0, y=0)

        image_1 = tk.PhotoImage(file=frame2_path + "image_1.png")
        add_element_button_image = tk.PhotoImage(file=frame2_path + "button_1.png")
        add_element_button = tk.Button(values_window, image=add_element_button_image, borderwidth=0,
                                       command=lambda: add_element(component_name), relief="flat")
        mag_entry = tk.Entry(values_window, bg="#D9D9D9", foreground="#780000", font=font)

        canvas.create_image(50.0, 20.0, image=image_1)
        add_element_button.place(x=140, y=75, width=82, height=15)
        mag_entry.place(x=15, y=40, width=52, height=18)

        magnitude = mag_entry.get()

        values_window.resizable(False, False)
        values_window.mainloop()


def pop_up_window(window):
    frame4_path = ASSETS_PATH + "\\frame4\\"
    pop_up = tk.Toplevel(window)
    pop_up.title("Warning")
    pop_up.geometry("155x100")
    pop_up.iconbitmap(frame4_path + "prohibition.ico")

    pop_up_message = tk.Label(pop_up, text="Maximum components \nreached.")
    close_button = tk.Button(pop_up, borderwidth=1, text="close", command=lambda: close_window(pop_up, window))
    pop_up_message.place(x=15, y=20)
    close_button.place(x=110, y=70, width=30, height=20)
    pop_up.resizable(False, False)
    pop_up.mainloop()


def close_window(pop_up, window):
    pop_up.destroy()
    window.deiconify()


def add_element(component_name):
    pass
