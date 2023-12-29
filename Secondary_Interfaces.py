import tkinter as tk
from tkinter import Canvas, ttk, PhotoImage, Button, Toplevel, Entry, Label

ASSETS_PATH = ".\\assets"
font = ('Times New Roman', 10, 'bold')
magnitude, angle, frequency, ramp_time, equation = None, None, None, None, None
branches, nodes = 0, 0


def set_values_window(window, component_name):
    global ASSETS_PATH, magnitude, angle, frequency, ramp_time, equation
    if component_name == 'AC':

        frame1_path = ASSETS_PATH + "\\frame1\\"
        values_window = Toplevel(window)
        values_window.title("Set Value")
        values_window.geometry("300x128")
        values_window.iconbitmap(frame1_path + "AC_Power.ico")
        values_window.focus_set()
        canvas = tk.Canvas(values_window, bg="#FFFFFF", height=150, width=300, bd=0)
        canvas.place(x=0, y=0)

        image_1 = PhotoImage(file=frame1_path + "image_1.png")
        image_2 = PhotoImage(file=frame1_path + "image_2.png")
        image_3 = PhotoImage(file=frame1_path + "image_3.png")
        image_4 = PhotoImage(file=frame1_path + "image_4.png")
        add_element_button_image = PhotoImage(file=frame1_path + "button_1.png")
        add_element_button = tk.Button(values_window, image=add_element_button_image, borderwidth=0,
                                       command=lambda: add_element(component_name))
        combobox_value = tk.StringVar()
        wave_type_combobox = ttk.Combobox(values_window, textvariable=combobox_value, state='readonly',
                                          values=['SINE', 'RECTANGLE', 'TRIANGLE', 'SAWTOOTH'])
        mag_entry = Entry(values_window, bg="#D9D9D9", foreground="#780000", font=font)
        ang_entry = Entry(values_window, bg="#D9D9D9", foreground="#780000", font=font)
        freq_entry = Entry(values_window, bg="#D9D9D9", foreground="#780000", font=font)
        ramp_entry = Entry(values_window, bg="#D9D9D9", foreground="#780000", font=font)
        eq_entry = Entry(values_window, bg="#D9D9D9", foreground="#780000", font=font)

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
        values_window = Toplevel(window)
        values_window.geometry("230x100")
        values_window.title("Set Value")
        values_window.iconbitmap(frame2_path + "DC.ico")
        values_window.focus_set()
        canvas = Canvas(values_window, bg="#FFFFFF", height=100, width=230, bd=0)
        canvas.place(x=0, y=0)

        image_1 = PhotoImage(file=frame2_path + "image_1.png")
        add_element_button_image = PhotoImage(file=frame2_path + "button_1.png")
        add_element_button = tk.Button(values_window, image=add_element_button_image, borderwidth=0,
                                       command=lambda: add_element(component_name), relief="flat")
        mag_entry = Entry(values_window, bg="#D9D9D9", foreground="#780000", font=font)

        canvas.create_image(50.0, 20.0, image=image_1)
        add_element_button.place(x=140, y=75, width=82, height=15)
        mag_entry.place(x=15, y=40, width=52, height=18)

        magnitude = mag_entry.get()

        values_window.resizable(False, False)
        values_window.mainloop()


def pop_up_window(window):
    frame4_path = ASSETS_PATH + "\\frame4\\"
    pop_up = Toplevel(window)
    pop_up.title("Warning")
    pop_up.geometry("155x100")
    pop_up.iconbitmap(frame4_path + "prohibition.ico")

    pop_up_message = Label(pop_up, text="Maximum components \nreached.")
    close_button = Button(pop_up, borderwidth=1, text="close", command=lambda: close_window(pop_up, window))
    pop_up_message.place(x=15, y=20)
    close_button.place(x=110, y=70, width=30, height=20)
    pop_up.resizable(False, False)
    pop_up.mainloop()


def process(window):
    frame5_path = ASSETS_PATH + "\\frame5\\"
    domain_window = Toplevel(window)
    domain_window.title("Domain")
    domain_window.geometry("158x84")
    domain_window.focus_set()
    canvas = tk.Canvas(domain_window, bg="#FFFFFF", height=84, width=158, bd=0)
    canvas.place(x=0, y=0)

    image_1 = PhotoImage(file=frame5_path + "image_1.png")
    image_2 = PhotoImage(file=frame5_path + "image_2.png")
    tmax_entry = Entry(domain_window, bg="#FFFFFF", foreground="#780000", font=font)
    step_entry = Entry(domain_window, bg="#FFFFFF", foreground="#780000", font=font)
    analyse_button_image = PhotoImage(file=frame5_path + "button_1.png")
    analyse_button = Button(domain_window, image=analyse_button_image, borderwidth=0,
                            command=lambda: analyse(domain_window, window), relief="flat")

    canvas.create_image(41.0, 18.0, image=image_1)
    canvas.create_image(113.0, 17.0, image=image_2)
    tmax_entry.place(x=25, y=30, width=30, height=18)
    step_entry.place(x=94, y=30, width=40, height=18)
    analyse_button.place(x=52.0, y=60.0, width=49, height=18.0)

    domain_window.resizable(False, False)
    domain_window.mainloop()


def analyse(domain_window, window):
    frame6_path = ASSETS_PATH + "\\frame6\\"
    result_window = Toplevel(window)
    result_window.title("Result")
    result_window.geometry("291x348")
    canvas = Canvas(result_window, bg="#FFFFFF", height=348, width=291, bd=0)
    canvas.place(x=0, y=0)

    close_window(domain_window, result_window)

    image_image_1 = PhotoImage(file=frame6_path + "image_1.png")
    image_image_2 = PhotoImage(file=frame6_path + "image_2.png")
    image_image_3 = PhotoImage(file=frame6_path + "image_3.png")
    image_image_4 = PhotoImage(file=frame6_path + "image_4.png")
    image_image_5 = PhotoImage(file=frame6_path + "image_5.png")
    image_image_6 = PhotoImage(file=frame6_path + "image_6.png")
    image_image_7 = PhotoImage(file=frame6_path + "image_7.png")
    image_image_8 = PhotoImage(file=frame6_path + "image_8.png")
    image_image_9 = PhotoImage(file=frame6_path + "image_9.png")

    branch_box = ttk.Combobox(result_window, state='readonly',
                              values=[f"Br. {i + 1}" for i in range(branches)])
    node_box = ttk.Combobox(result_window, state='readonly',
                            values=[f"{i + 1}" for i in range(nodes)])
    from_box = ttk.Combobox(result_window, state='readonly',
                            values=[f"{i + 1}" for i in range(nodes)])
    to_box = ttk.Combobox(result_window, state='readonly',
                          values=[f"{i + 1}" for i in range(nodes)])

    tmin_branch_entry = Entry(result_window, bg="#FFFFFF", foreground="#780000", font=font)
    tmax_branch_entry = Entry(result_window, bg="#FFFFFF", foreground="#780000", font=font)
    tmin_node_entry = Entry(result_window, bg="#FFFFFF", foreground="#780000", font=font)
    tmax_node_entry = Entry(result_window, bg="#FFFFFF", foreground="#780000", font=font)
    from_to_tmin_entry = Entry(result_window, bg="#FFFFFF", foreground="#780000", font=font)
    from_to_tmax_entry = Entry(result_window, bg="#FFFFFF", foreground="#780000", font=font)

    plot_branch_button_image = PhotoImage(file=frame6_path + "button_1.png")
    plot_branch_button = Button(result_window, image=plot_branch_button_image, borderwidth=0,
                                command=lambda: print("button_1 clicked"), relief="flat")
    plot_node_button_image = PhotoImage(file=frame6_path + "button_2.png")
    plot_node_button = Button(result_window, image=plot_node_button_image, borderwidth=0,
                              command=lambda: print("button_2 clicked"), relief="flat")
    plot_from_to_button_image = PhotoImage(file=frame6_path + "button_3.png")
    plot_from_to_button = Button(result_window, image=plot_from_to_button_image, borderwidth=0,
                                 command=lambda: print("button_3 clicked"), relief="flat")
    export_button_image = PhotoImage(file=frame6_path + "button_4.png")
    export_button = Button(result_window, image=export_button_image, borderwidth=0,
                           command=lambda: print("button_4 clicked"), relief="flat")

    canvas.create_image(47.0, 30.0, image=image_image_1)
    canvas.create_image(46.0, 131.0, image=image_image_2)
    canvas.create_image(66.0, 226.0, image=image_image_3)
    canvas.create_image(128.0, 148.0, image=image_image_4)
    canvas.create_image(196.0, 147.0, image=image_image_5)
    canvas.create_image(128.0, 261.0, image=image_image_6)
    canvas.create_image(196.0, 260.0, image=image_image_7)
    canvas.create_image(128.0, 58.0, image=image_image_8)
    canvas.create_image(196.0, 57.0, image=image_image_9)

    branch_box.place(x=25, y=50, width=45, height=18)
    node_box.place(x=25, y=152, width=45, height=18)
    from_box.place(x=15, y=246, width=35, height=18)
    to_box.place(x=60, y=246, width=35, height=18)
    tmin_branch_entry.place(x=108, y=80, width=40, height=18)
    tmax_branch_entry.place(x=176, y=80, width=40, height=18)
    tmin_node_entry.place(x=108, y=170, width=40, height=18)
    tmax_node_entry.place(x=176, y=170, width=40, height=18)
    from_to_tmin_entry.place(x=108, y=280, width=40, height=18)
    from_to_tmax_entry.place(x=176, y=280, width=40, height=18)
    plot_branch_button.place(x=238.0, y=61.0, width=44.0, height=18.0)
    plot_node_button.place(x=237.0, y=164.0, width=44.0, height=18.0)
    plot_from_to_button.place(x=237.0, y=267.0, width=44.0, height=18.0)
    export_button.place(x=85.0, y=304.0, width=118.0, height=31.0)

    result_window.resizable(False, False)
    result_window.mainloop()


def add_element(component_name):
    pass


def close_window(pop_up, window):
    window.focus_set()
    pop_up.destroy()


def set_nodes(last_node):
    global nodes
    if nodes < last_node:
        nodes = last_node
    print(nodes)
