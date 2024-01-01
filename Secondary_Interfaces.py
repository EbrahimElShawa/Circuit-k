import tkinter as tk
from tkinter import Canvas, ttk, PhotoImage, Button, Toplevel, Entry, Label, StringVar

from sympy import sympify, symbols

from Main_Interface import run_circuit
import circuitTools

main_interface, loading_window = tk.NONE, tk.NONE
main_circuit = None
ASSETS_PATH = r"./assets"
idle_font = ('Times New Roman', 8, 'italic')
active_font = ('Times New Roman', 10, 'bold')
branches, nodes = 0, 0
component_list, magnitude_list, ramp_time_list, nodes_list = [], [], [], []
wave_type_list, angle_list, freq_list = [], [], []
max_time, step = '', ''
Dummy_Value = '-1'


def welcome_screen(main):
    global main_interface
    frame0_path = ASSETS_PATH + '/frame0/'
    main_interface = main
    width, height = 587, 400
    x, y = get_geometry(width, height)

    window = Toplevel(main_interface)
    window.geometry(f"{width}x{height}+{x}+{y}")
    window.configure(bg="#FFFFFF")
    window.title('Circuit K')
    canvas = Canvas(window, bg="#FFFFFF", height=400, width=578, bd=0)
    canvas.place(x=0, y=0)

    image_1 = PhotoImage(file=frame0_path + "image_1.png")
    canvas.create_image(287.0, 200.0, image=image_1)

    credit_button_image = PhotoImage(
        file=frame0_path + "button_1.png")
    credit_button = Button(window, image=credit_button_image, borderwidth=0,
                           command=lambda: credit_window(window))
    credit_button.place(x=535.0, y=11.0, width=30.0, height=30.0)

    start_button_image = PhotoImage(file=frame0_path + "button_2.png")
    start_button = Button(window, image=start_button_image, borderwidth=0,
                          command=lambda: window.destroy())
    start_button.place(x=442.0, y=346.0, width=118.0, height=44.0)

    image_2 = PhotoImage(file=frame0_path + "image_2.png")
    canvas.create_image(289.0, 167.0, image=image_2)

    image_3 = PhotoImage(file=frame0_path + "image_3.png")
    canvas.create_image(289.0, 279.0, image=image_3)

    image_4 = PhotoImage(file=frame0_path + "image_4.png")
    canvas.create_image(295.0, 81.0, image=image_4)

    image_5 = PhotoImage(file=frame0_path + "image_5.png")
    canvas.create_image(289.0, 205.0, image=image_5)

    window.transient(main_interface)
    window.protocol('WM_DELETE_WINDOW', lambda: main_interface.grap_relese())
    window.grab_set()
    window.mainloop()


def credit_window(welcome_window):
    frame1_path = ASSETS_PATH + '/frame1/'
    width, height = 504, 409
    x, y = get_geometry(width, height)

    window = Toplevel(welcome_window)
    window.geometry(f"{width}x{height}+{x}+{y}")
    window.configure(bg="#FFFFFF")
    window.focus_set()
    canvas = Canvas(window, bg="#FFFFFF", height=409, width=504, bd=0)

    canvas.place(x=0, y=0)
    image_image_1 = PhotoImage(file=frame1_path + "image_1.png")
    canvas.create_image(250.0, 204.0, image=image_image_1)

    image_image_2 = PhotoImage(file=frame1_path + "image_2.png")
    canvas.create_image(252.0, 41.0, image=image_image_2)

    image_image_3 = PhotoImage(file=frame1_path + "image_3.png")
    canvas.create_image(222.0, 131.0, image=image_image_3)

    image_image_4 = PhotoImage(file=frame1_path + "image_4.png")
    canvas.create_image(250.0, 264.0, image=image_image_4)

    close_button_image = PhotoImage(file=frame1_path + "button_1.png")
    close_button = Button(window, image=close_button_image, borderwidth=0,
                          command=lambda: window.destroy())
    close_button.place(x=414.0, y=359.0, width=68.0, height=33.0)

    window.transient(welcome_window)
    window.mainloop()


def set_values_window(w, index, component_name):
    global main_interface
    main_interface = w
    if component_name in ['R', 'L', 'C']:
        frame4_path = ASSETS_PATH + "/frame4/"
        width, height = 280, 120
        x, y = get_geometry(width, height)
        values_window = Toplevel(main_interface)
        values_window.geometry(f"{width}x{height}+{x}+{y}")
        values_window.title("Set Value")
        # values_window.iconbitmap(frame2_path + 'DC.ico')
        canvas = Canvas(values_window, bg="#FFFFFF", height=120, width=280, bd=0)
        canvas.place(x=0, y=0)

        image_1 = PhotoImage(file=frame4_path + "image_1.png")
        add_element_button_image = PhotoImage(file=frame4_path + "button_1.png")
        mag_entry = Entry(values_window, bg="#D9D9D9", foreground="#780000", font=active_font)
        add_element_button = tk.Button(values_window, image=add_element_button_image, borderwidth=0,
                                       command=lambda: add_element(values_window, component_name,
                                                                   mag_entry.get(), index))
        values_window.transient(main_interface)
        mag_entry.focus_set()
        mag_entry.bind("<Return>", lambda event: add_element_button.invoke())

        canvas.create_image(74, 24, image=image_1)
        mag_entry.place(x=35, y=48, width=80, height=20)
        add_element_button.place(x=140, y=78, width=121.5, height=32)

        values_window.mainloop()

    elif component_name == 'AC':
        frame3_path = ASSETS_PATH + "/frame3/"
        width, height = 300, 128
        x, y = get_geometry(width, height)
        values_window = Toplevel(main_interface)
        values_window.title("Set Value")
        values_window.geometry(f"{width}x{height}+{x}+{y}")
        # values_window.iconbitmap(frame1_path + 'AC_Power.ico')

        canvas = tk.Canvas(values_window, bg="#FFFFFF", height=150, width=300, bd=0)
        canvas.place(x=0, y=0)

        image_1 = PhotoImage(file=frame3_path + "image_1.png")
        image_2 = PhotoImage(file=frame3_path + "image_2.png")
        add_element_button_image = PhotoImage(file=frame3_path + "button_1.png")
        add_element_button = tk.Button(values_window, image=add_element_button_image, borderwidth=0,
                                       command=lambda: add_source(values_window, mag_entry.get(),
                                                                  ang_entry.get(), freq_entry.get(),
                                                                  ramp_entry.get(), source_type_combobox.get(),
                                                                  wave_type_combobox.get(), index))
        source_type_combobox = ttk.Combobox(values_window, state='readonly', values=['Vac', 'Iac'])
        wave_type_combobox = ttk.Combobox(values_window, state='readonly',
                                          values=['SINE', 'RECTANGLE', 'TRIANGLE', 'SAWTOOTH'])
        mag_entry = Entry(values_window, bg="#D9D9D9", foreground="#780000", font=active_font)
        ang_entry = Entry(values_window, bg="#D9D9D9", foreground="#780000", font=active_font)
        freq_entry = Entry(values_window, bg="#D9D9D9", foreground="#780000", font=active_font)
        ramp_entry = Entry(values_window, bg="#D9D9D9", foreground="#780000", font=active_font)

        values_window.transient(main_interface)
        mag_entry.focus_set()
        source_type_combobox.set('Vac')
        wave_type_combobox.set('SINE')
        mag_entry.bind('<Return>', lambda event: add_element_button.invoke())
        ang_entry.bind('<Return>', lambda event: add_element_button.invoke())
        freq_entry.bind('<Return>', lambda event: add_element_button.invoke())
        ramp_entry.bind('<Return>', lambda event: add_element_button.invoke())

        canvas.create_image(36, 17, image=image_1)
        canvas.create_image(188, 17, image=image_2)
        source_type_combobox.place(x=20, y=90, width=40, height=20)
        wave_type_combobox.place(x=70, y=90, width=90, height=20)
        add_element_button.place(x=210, y=106, width=82, height=15)
        mag_entry.place(x=8, y=35, width=52, height=18)
        ang_entry.place(x=85, y=35, width=32, height=18)
        freq_entry.place(x=148, y=35, width=30, height=18)
        ramp_entry.place(x=220, y=35, width=30, height=18)

        values_window.mainloop()

    elif component_name in ['Idc', 'Vdc']:
        frame4_path = ASSETS_PATH + "/frame4/"
        width, height = 300, 135
        x, y = get_geometry(width, height)
        values_window = Toplevel(main_interface)
        values_window.geometry(f"{width}x{height}+{x}+{y}")
        values_window.title("Set Value")
        # values_window.iconbitmap(frame2_path + 'DC.ico')
        canvas = Canvas(values_window, bg="#FFFFFF", height=135, width=300, bd=0)
        canvas.place(x=0, y=0)

        image_1 = PhotoImage(file=frame4_path + "image_1.png")
        image_2 = PhotoImage(file=frame4_path + "image_2.png")
        add_element_button_image = PhotoImage(file=frame4_path + "button_2.png")
        mag_entry = Entry(values_window, bg="#D9D9D9", foreground="#780000", font=active_font)
        ramp_entry = Entry(values_window, bg="#D9D9D9", foreground="#780000", font=active_font)
        add_element_button = tk.Button(values_window, image=add_element_button_image, borderwidth=0,
                                       command=lambda: add_source(values_window, mag_entry.get(), -1, -1,
                                                                  ramp_entry.get(), component_name, "DC", index))

        values_window.transient(main_interface)
        mag_entry.focus_set()
        mag_entry.bind('<Return>', lambda event: add_element_button.invoke())
        ramp_entry.bind('<Return>', lambda event: add_element_button.invoke())

        canvas.create_image(74, 22, image=image_1)
        canvas.create_image(222, 22, image=image_2)
        add_element_button.place(x=89, y=90, width=121.5, height=32)
        mag_entry.place(x=35, y=50, width=70, height=20)
        ramp_entry.place(x=195, y=50, width=60, height=20)

        values_window.mainloop()

    else:  # Equation
        frame5_path = ASSETS_PATH + "/frame5/"
        width, height = 260, 150
        x, y = get_geometry(width, height)
        values_window = Toplevel(main_interface)
        values_window.geometry(f"{width}x{height}+{x}+{y}")
        values_window.title('Write equation')
        # values_window.iconbitmap(frame3_path + 'more.ico')
        values_window.focus_set()
        canvas = Canvas(values_window, bg="#FFFFFF", height=150, width=300, bd=0)
        canvas.place(x=0, y=0)

        image_1 = PhotoImage(file=frame5_path + "image_1.png")
        eq_entry = Entry(values_window, bg="#D9D9D9", foreground="#780000", font=idle_font)
        source_type_combobox = ttk.Combobox(values_window, state='readonly', values=['Voltage', 'Current'])
        add_element_button_image = PhotoImage(file=frame5_path + "button_1.png")
        add_element_button = Button(values_window, image=add_element_button_image, borderwidth=0,
                                    command=lambda: add_equation(values_window, eq_entry.get(),
                                                                 source_type_combobox.get(), index))

        values_window.transient(main_interface)
        initial_comment = 'Equation in param t'
        eq_entry.insert(0, initial_comment)
        eq_entry.bind('<FocusIn>', lambda event: configure_entry(eq_entry, initial_comment))
        eq_entry.bind('<Return>', lambda event: add_element_button.invoke())

        canvas.create_image(71.0, 28.0, image=image_1)
        eq_entry.place(x=20, y=58, width=125, height=22)
        source_type_combobox.place(x=165, y=58, width=70, height=22)
        add_element_button.place(x=125, y=109.0, width=121.5, height=32.)

        values_window.mainloop()


def pop_up_window(w):
    global main_interface
    main_interface = w
    # frame6_path = ASSETS_PATH + "/frame6/"
    width, height = 155, 80
    x, y = get_geometry(width, height)
    pop_up = Toplevel(main_interface)
    pop_up.title("Warning")
    # pop_up.iconbitmap(frame6_path + 'prohibition.ico')
    pop_up.geometry(f"{width}x{height}+{x}+{y}")

    pop_up_message = Label(pop_up, text="Max reached.")
    close_button = Button(pop_up, borderwidth=1, text="close", command=lambda: close_window(pop_up))
    pop_up_message.place(x=15, y=15)
    close_button.place(x=107.5, y=60, width=35, height=20)

    pop_up.transient(main_interface)
    pop_up.focus_set()
    pop_up.mainloop()


def process_window(w):
    global main_interface
    main_interface = w
    frame7_path = ASSETS_PATH + "/frame7/"
    width, height = 195, 110
    x, y = get_geometry(width, height)
    domain_window = Toplevel(main_interface)
    domain_window.title("Domain")
    domain_window.geometry(f"{width}x{height}+{x}+{y}")
    domain_window.focus_set()
    canvas = tk.Canvas(domain_window, bg="#FFFFFF", height=110, width=195, bd=0)
    canvas.place(x=0, y=0)

    image_1 = PhotoImage(file=frame7_path + "image_1.png")
    image_2 = PhotoImage(file=frame7_path + "image_2.png")
    tmax_entry = Entry(domain_window, bg="#FFFFFF", foreground="#780000", font=active_font)
    step_entry = Entry(domain_window, bg="#FFFFFF", foreground="#780000", font=idle_font)
    analyse_button_image = PhotoImage(file=frame7_path + "button_1.png")
    analyse_button = Button(domain_window, image=analyse_button_image, borderwidth=0,
                            command=lambda: analyse(domain_window, main_interface, tmax_entry.get(), step_entry.get()))

    domain_window.transient(main_interface)
    tmax_entry.focus_set()
    tmax_entry.bind('<Return>', lambda event: analyse_button.invoke())
    step_entry.insert(0, '1e-4')
    step_entry.bind('<FocusIn>', lambda event: configure_entry(step_entry))
    step_entry.bind('<Return>', lambda event: analyse_button.invoke())

    canvas.create_image(54, 24, image=image_1)
    canvas.create_image(140, 24, image=image_2)
    tmax_entry.place(x=35, y=45, width=40, height=18)
    step_entry.place(x=120, y=45, width=40, height=18)
    analyse_button.place(x=60, y=73, width=62, height=25)

    domain_window.mainloop()


def analyse(domain_window, w, t_max, t_step):
    global main_interface, max_time, step, nodes, main_circuit
    main_interface = w
    try:
        _, _ = float(t_max), float(t_step)
    except ValueError:
        print('Please enter a valid number')
        return
    max_time, step = t_max, t_step

    from create_files import create_time_file
    create_time_file(max_time, step)
    main_circuit = run_circuit()

    frame8_path = ASSETS_PATH + "/frame8/"
    width, height = 291, 348
    x, y = get_geometry(width, height)
    result_window = Toplevel(main_interface)
    result_window.title("Result")
    result_window.geometry(f"{width}x{height}+{x}+{y}")
    canvas = Canvas(result_window, bg="#FFFFFF", height=348, width=291, bd=0)
    canvas.place(x=0, y=0)
    close_pop_up(domain_window, result_window)

    image_image_1 = PhotoImage(file=frame8_path + "image_1.png")
    image_image_2 = PhotoImage(file=frame8_path + "image_2.png")
    image_image_3 = PhotoImage(file=frame8_path + "image_3.png")
    image_image_4 = PhotoImage(file=frame8_path + "image_4.png")
    image_image_5 = PhotoImage(file=frame8_path + "image_5.png")
    image_image_6 = PhotoImage(file=frame8_path + "image_6.png")
    image_image_7 = PhotoImage(file=frame8_path + "image_7.png")
    image_image_8 = PhotoImage(file=frame8_path + "image_8.png")
    image_image_9 = PhotoImage(file=frame8_path + "image_9.png")

    branch_box = ttk.Combobox(result_window, state='readonly',
                              values=[f"{i + 1}" for i in range(branches)])
    node_box = ttk.Combobox(result_window, state='readonly',
                            values=[f"{i + 1}" for i in range(nodes)])
    from_box = ttk.Combobox(result_window, state='readonly',
                            values=[f"{i + 1}" for i in range(nodes)])
    to_box = ttk.Combobox(result_window, state='readonly',
                          values=[f"{i + 1}" for i in range(nodes)])

    tmin_branch_entry = Entry(result_window, bg="#FFFFFF", foreground="#780000", font=active_font)
    tmax_branch_entry = Entry(result_window, bg="#FFFFFF", foreground="#780000", font=active_font)
    tmin_node_entry = Entry(result_window, bg="#FFFFFF", foreground="#780000", font=active_font)
    tmax_node_entry = Entry(result_window, bg="#FFFFFF", foreground="#780000", font=active_font)
    from_to_tmin_entry = Entry(result_window, bg="#FFFFFF", foreground="#780000", font=active_font)
    from_to_tmax_entry = Entry(result_window, bg="#FFFFFF", foreground="#780000", font=active_font)

    plot_branch_button_image = PhotoImage(file=frame8_path + "button_1.png")
    plot_branch_button = Button(result_window, image=plot_branch_button_image, borderwidth=0,
                                command=lambda: plot_branch(branch_box.get(), tmin_branch_entry.get(),
                                                            tmax_branch_entry.get()))
    plot_node_button_image = PhotoImage(file=frame8_path + "button_2.png")
    plot_node_button = Button(result_window, image=plot_node_button_image, borderwidth=0,
                              command=lambda: plot_node(node_box.get(), tmin_node_entry.get(), tmax_node_entry.get()))
    plot_from_to_button_image = PhotoImage(file=frame8_path + "button_3.png")
    plot_from_to_button = Button(result_window, image=plot_from_to_button_image, borderwidth=0,
                                 command=lambda: plot_from_to(from_box.get(), to_box.get(),
                                                              from_to_tmin_entry.get(), from_to_tmax_entry.get()))
    export_button_image = PhotoImage(file=frame8_path + "button_4.png")
    export_button = Button(result_window, image=export_button_image, borderwidth=0,
                           command=lambda: csv_file())

    result_window.transient(main_interface)
    tmin_branch_entry.insert(0, '0')
    tmin_node_entry.insert(0, '0')
    from_to_tmin_entry.insert(0, '0')
    tmax_branch_entry.insert(0, f'{t_max}')
    tmax_node_entry.insert(0, f'{t_max}')
    from_to_tmax_entry.insert(0, f'{t_max}')
    tmin_branch_entry.bind('<FocusIn>', lambda event: configure_entry(tmin_branch_entry))
    tmin_node_entry.bind('<FocusIn>', lambda event: configure_entry(tmin_node_entry))
    from_to_tmin_entry.bind('<FocusIn>', lambda event: configure_entry(from_to_tmin_entry))
    tmax_branch_entry.bind('<FocusIn>', lambda event: configure_entry(tmax_branch_entry))
    tmax_node_entry.bind('<FocusIn>', lambda event: configure_entry(tmax_node_entry))
    from_to_tmax_entry.bind('<FocusIn>', lambda event: configure_entry(from_to_tmax_entry))

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
    plot_branch_button.place(x=238.0, y=80, width=44.0, height=18.0)
    plot_node_button.place(x=237.0, y=170, width=44.0, height=18.0)
    plot_from_to_button.place(x=237.0, y=280, width=44.0, height=18.0)
    export_button.place(x=85.0, y=310, width=118.0, height=31.0)

    result_window.mainloop()


def update(new_percentage, cur_sec):
    bar['value'] = cur_sec
    percent.set(str(round(new_percentage, 2)) + "%")
    text.set(str(round(cur_sec, 5)) + "/" + str(max_time) + " second completed")
    loading_window.update_idletasks()
    if bar['value'] == float(max_time):
        close_window(loading_window)


def progress_bar_window():
    global loading_window, percent, text, bar, cur
    cur = 0
    width, height = 320, 80
    x, y = get_geometry(width, height)
    loading_window = Toplevel()
    loading_window.title("Loading....")
    loading_window.geometry(f"{width}x{height}+{x}+{y}")
    canvas = Canvas(loading_window, bg='#FFFFFF', width=width, height=height, bd=0)
    canvas.place(x=0, y=0)
    percent = StringVar()
    text = StringVar()

    bar = ttk.Progressbar(loading_window, orient=tk.HORIZONTAL, length=300, mode='determinate', maximum=float(max_time))
    bar.pack(pady=10)

    Label(loading_window, textvariable=percent, bg='#FFFFFF').pack()
    Label(loading_window, textvariable=text, bg='#FFFFFF').pack()

    loading_window.transient(main_interface)
    loading_window.focus_set()


def add_source(values_window, mag, ang, freq, ramp, source_type, wave_type, index):
    global magnitude_list, component_list, ramp_time_list, freq_list, angle_list, wave_type_list

    print(magnitude_list)
    print(index)

    input_value = [mag, ang, freq, ramp]
    try:
        for _ in input_value:
            __ = float(_)
    except ValueError:
        print('Please enter a valid number')
        return
    close_window(values_window)

    magnitude_list[index] = mag
    component_list[index] = source_type
    ramp_time_list[index] = ramp
    freq_list[index] = freq
    wave_type_list[index] = wave_type
    angle_list[index] = ang


def add_element(values_window, component_name, mag, index):
    global component_list, magnitude_list, ramp_time_list, freq_list, wave_type_list, angle_list
    try:
        _ = float(mag)
    except ValueError:
        print('Please enter a valid number')
        return
    close_window(values_window)

    print(magnitude_list)
    print(index)

    component_list[index] = component_name
    magnitude_list[index] = mag
    ramp_time_list[index] = Dummy_Value
    freq_list[index] = Dummy_Value
    wave_type_list[index] = Dummy_Value
    angle_list[index] = Dummy_Value


def add_equation(values_window, eq, source_type, index):
    global component_list, magnitude_list, ramp_time_list, freq_list, wave_type_list, angle_list
    try:
        t = symbols('t')
        expr = sympify(eq)
        result = expr.subs(t, 1).evalf()
        _ = float(result)
    except ValueError:
        print('Please enter a valid expression ( equation in t )')
        return
    close_window(values_window)

    if source_type == 'Voltage':
        component_list[index] = 'Veq'
    else:
        component_list[index] = 'Ieq'
    magnitude_list[index] = eq
    ramp_time_list[index] = Dummy_Value
    freq_list[index] = Dummy_Value
    wave_type_list[index] = eq
    angle_list[index] = Dummy_Value


def plot_branch(branch, t_min, t_max):
    try:
        _, _, _ = int(branch[-1]), float(t_min), float(t_max)
    except IndexError:
        print('Please select a branch')
        return
    except ValueError:
        print('Please enter a valid number')
        return

    circuitTools.plot_branch(main_circuit, 0, int(branch), Dummy_Value, t_min, t_max)


def plot_node(node, t_min, t_max):
    if node == '':
        print('Please select a node')
        return
    try:
        _, _ = float(t_min), float(t_max)
    except ValueError:
        print('Please enter a valid number')
        return

    circuitTools.plot_branch(main_circuit, 1, int(node), Dummy_Value, t_min, t_max)


def plot_from_to(from_node, to_node, t_min, t_max):
    if from_node == '' or to_node == '':
        print('Please select nodes')
        return
    try:
        _, _, = float(t_min), float(t_max)
    except ValueError:
        print('Please enter a valid number')
        return

    circuitTools.plot_branch(main_circuit, 2, int(from_node), int(to_node), t_min, t_max)


def csv_file():
    circuitTools.excel(main_circuit)


def max_node():
    global nodes
    for x, y in nodes_list:
        nodes = max(int(x), int(y), int(nodes))


def close_window(child):
    main_interface.focus_set()
    child.destroy()


def close_pop_up(child, parent):
    parent.focus_set()
    child.destroy()


def get_geometry(width, height):
    screen_center = [1920 / 2, 1080 / 2]
    x = int(screen_center[0] - width / 2)
    y = int(screen_center[1] - height / 2)
    return x, y


def configure_entry(entry, text=''):
    if entry.get() == text:
        entry.delete(0, tk.END)
    else:
        entry.selection_range(0, tk.END)
    entry.config(font=active_font)
