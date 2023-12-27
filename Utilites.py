from pathlib import Path
import tkinter as tk
from tkinter import Button, PhotoImage, ttk, Canvas
import Secondary_Interfaces

OUTPUT_PATH = Path(__file__).parent
add_button_count = 0
entries_and_buttons, label_button_set = [], []
set_values_button, its_label = tk.NONE, tk.NONE
ASSETS_PATH = Path("P:\\Study\\Python\\Tick_2\\assets")


def add_fields(window):
    global add_button_count, entries_and_buttons, label_button_set

    if not entries_and_buttons:
        new_y = 115  # Initial position
    else:
        last_entry_set = entries_and_buttons[-1]
        last_entry = last_entry_set[0]
        last_y = int(last_entry.place_info()['y'])
        new_y = last_y + 27

    combobox_value = tk.StringVar()
    from_entry = tk.Entry(window, bg="#D9D9D9", foreground="#0500FF", font=('Times New Roman', 15, 'bold'))
    to_entry = tk.Entry(window, bg="#D9D9D9", foreground="#0500FF", font=('Times New Roman', 15, 'bold'))
    component_type_combobox = ttk.Combobox(window, textvariable=combobox_value, state='readonly',
                                           values=['R', 'L', 'C', 'Vs', 'Is', 'AC'])
    component_type_combobox.bind("<<ComboboxSelected>>",
                                 lambda event: create_new_component(component_type_combobox, new_y, window))
    remove_button_image = PhotoImage(file=ASSETS_PATH / "frame0\\button_5.png")
    remove_button = Button(image=remove_button_image, borderwidth=0,
                           command=lambda: remove(from_entry, to_entry, component_type_combobox, remove_button))
    remove_button.image = remove_button_image  # :)    Keeping a reference to the image for newly created buttons
    # Because only once can an Image be an instance for a button (can't be for multiple buttons)

    from_entry.place(x=105, y=new_y, width=36, height=22)
    to_entry.place(x=180, y=new_y, width=36, height=22)
    component_type_combobox.place(x=250, y=new_y, width=52, height=22)
    remove_button.place(x=369, y=new_y, width=107.0, height=22.0)

    add_button_count += 1
    entries_and_buttons.append((from_entry, to_entry, component_type_combobox, remove_button))


def remove(from_entry, to_entry, type_combobox, remove_button):
    global entries_and_buttons, label_button_set, add_button_count, set_values_button, its_label
    e_index = entries_and_buttons.index((from_entry, to_entry, type_combobox, remove_button))
    if label_button_set:
        l_index = label_button_set.index((set_values_button, its_label))

    from_entry.destroy()
    to_entry.destroy()
    remove_button.destroy()

    if label_button_set:
        label_button_set.remove((set_values_button, its_label))
        if set_values_button is not None:
            set_values_button.destroy()
            its_label.destroy()
        for i in range(l_index, len(label_button_set)):
            widget_set = label_button_set[i]
            for widget in widget_set:
                place_info = widget.place_info()
                widget.place(x=int(place_info['x']), y=int(place_info['y']) - 27)
    add_button_count -= 1

    entries_and_buttons.remove((from_entry, to_entry, type_combobox, remove_button))
    for i in range(e_index, len(entries_and_buttons)):  # Repositioning later instances
        widget_set = entries_and_buttons[i]
        for widget in widget_set:
            place_info = widget.place_info()
            widget.place(x=int(place_info['x']), y=int(place_info['y']) - 27)

    if not entries_and_buttons:
        add_button_count = 0


def clear_all():
    global entries_and_buttons

    for entry_set in entries_and_buttons:
        for entry in entry_set:
            entry.destroy()

    entries_and_buttons = []


def create_new_component(type_combobox, y, window):
    global set_values_button, its_label, label_button_set
    component_name = type_combobox.get()
    its_label = tk.Label(window, text=component_name, bg="#D9D9D9",
                         font=('Times New Roman', 15, 'bold'), foreground="#003049")
    its_label.place(x=60, y=y - 2)  # Minor adjustment to y-axis
    type_combobox.destroy()

    set_values_button = tk.Button(window, text="Set value", borderwidth=0,
                                  command=lambda: Secondary_Interfaces.set_values_window(window, component_name))
    set_values_button.place(x=250, y=y)

    label_button_set.append((set_values_button, its_label))
