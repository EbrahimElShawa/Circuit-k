import tkinter as tk
from tkinter import Button, PhotoImage, ttk
import Secondary_Interfaces
import circuitTools
import create_files

widgets_sets_count = 0
widgets_set = []
ASSETS_PATH = r"./assets/"


def add_fields(window):
    global widgets_sets_count, widgets_set

    if widgets_sets_count >= 12:
        Secondary_Interfaces.pop_up_window(window)
        return

    if not widgets_set:
        new_y = 115  # Initial position
    else:
        last_widget_set = widgets_set[-1]
        last_widget = last_widget_set[0]
        last_y = int(last_widget.place_info()['y'])
        new_y = last_y + 27

    from_entry = tk.Entry(window, bg="#D9D9D9", foreground="#0500FF", font=('Times New Roman', 15, 'bold'))
    to_entry = tk.Entry(window, bg="#D9D9D9", foreground="#0500FF", font=('Times New Roman', 15, 'bold'))
    component_type_combobox = ttk.Combobox(window, state='readonly',
                                           values=['R', 'L', 'C', 'Equation', 'Vdc', 'Idc', 'AC'])
    component_label = tk.Label(window, text=f"{widgets_sets_count + 1}", bg="#D9D9D9",
                               font=('Times New Roman', 15, 'bold'), foreground="#003049")
    remove_button_image = PhotoImage(file=ASSETS_PATH + "frame0/button_5.png")
    remove_button = Button(image=remove_button_image, borderwidth=0, command=lambda: remove(widget_set))
    remove_button.image = remove_button_image  # :)    Keeping a reference to the image for newly created buttons
    # Because only once can an Image be an instance for a button (can't be for multiple buttons)
    window.focus_set()

    from_entry.place(x=105, y=new_y, width=36, height=22)
    to_entry.place(x=180, y=new_y, width=36, height=22)
    component_type_combobox.place(x=250, y=new_y, width=52, height=22)
    remove_button.place(x=369, y=new_y, width=107.0, height=22.0)
    component_label.place(x=60, y=new_y - 2)  # Minor adjustment to y-axis

    component_type_combobox.bind("<<ComboboxSelected>>",
                                 lambda event: Secondary_Interfaces.set_values_window(window,
                                                                                      widgets_set.index(widget_set),
                                                                                      component_type_combobox.get()))
    Secondary_Interfaces.branches = int(component_label.cget("text"))

    Secondary_Interfaces.magnitude_list.append('')
    Secondary_Interfaces.component_list.append('')
    Secondary_Interfaces.ramp_time_list.append('')
    Secondary_Interfaces.angle_list.append('')
    Secondary_Interfaces.freq_list.append('')
    Secondary_Interfaces.wave_type_list.append('')
    Secondary_Interfaces.nodes_list.append(('', ''))

    widget_set = (from_entry, to_entry, component_type_combobox, remove_button, component_label)
    widgets_sets_count += 1
    widgets_set.append(widget_set)


def validate(window, select=''):
    print("checking that all boxes filled")
    print(Secondary_Interfaces.magnitude_list, Secondary_Interfaces.angle_list, Secondary_Interfaces.freq_list,
          Secondary_Interfaces.component_list
          , Secondary_Interfaces.ramp_time_list, Secondary_Interfaces.wave_type_list, Secondary_Interfaces.nodes_list)
    global widgets_set

    if len(widgets_set) == 0:
        return

    for i, a in enumerate(widgets_set):
        Secondary_Interfaces.nodes_list[i] = (a[0].get(), a[1].get())

    for value in Secondary_Interfaces.nodes_list:
        if value[0] == '' or value[1] == '':
            print("There are empty boxes")
            return
    for value in Secondary_Interfaces.magnitude_list:
        if value == '':
            print("There are empty boxes")
            return

    for value in Secondary_Interfaces.ramp_time_list:
        if value == '':
            print("There are empty boxes")
            return

    create_files.delete_files()
    create_files.netlist()

    if select == 'Schema':
        circuitTools.picture()
    else:
        Secondary_Interfaces.max_node()

        Secondary_Interfaces.process_window(window)


def remove(widgets):
    global widgets_set, widgets_sets_count
    index = widgets_set.index(widgets)

    print(index)

    for widget in widgets:
        widget.destroy()
    widgets_set.remove(widgets)
    Secondary_Interfaces.nodes_list.pop(index)
    Secondary_Interfaces.magnitude_list.pop(index)
    Secondary_Interfaces.component_list.pop(index)
    Secondary_Interfaces.wave_type_list.pop(index)
    Secondary_Interfaces.freq_list.pop(index)
    Secondary_Interfaces.angle_list.pop(index)
    Secondary_Interfaces.ramp_time_list.pop(index)

    print(Secondary_Interfaces.magnitude_list)

    if widgets_sets_count == 1:
        clear_all()
        return
    widgets_sets_count -= 1
    Secondary_Interfaces.branches -= 1

    for i in range(index, len(widgets_set)):  # Reconfiguring later instances
        widget_set = widgets_set[i]
        for widget in widget_set:
            place_info = widget.place_info()
            widget.place(x=int(place_info['x']), y=int(place_info['y']) - 27)
        element = widget_set[4].cget("text")
        widget_set[4].configure(text=f"{int(element) - 1}")


def clear_all():
    global widgets_set, widgets_sets_count

    for widget_set in widgets_set:
        for widget in widget_set:
            widget.destroy()

    widgets_sets_count = 0
    Secondary_Interfaces.nodes = 0
    Secondary_Interfaces.branches = 0
    widgets_set = []
    Secondary_Interfaces.nodes_list = []
    Secondary_Interfaces.component_list = []
    Secondary_Interfaces.magnitude_list = []
    Secondary_Interfaces.ramp_time_list = []
    Secondary_Interfaces.freq_list = []
    Secondary_Interfaces.wave_type_list = []
    Secondary_Interfaces.angle_list = []
