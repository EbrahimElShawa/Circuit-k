from pathlib import Path
import tkinter as tk
from tkinter import Button, PhotoImage, ttk, Canvas
import Secondary_Interfaces

OUTPUT_PATH = Path(__file__).parent
widgets_sets_count = 0
widgets_set = []
ASSETS_PATH = Path("P:\\Study\\Python\\Tick_2\\assets")


def add_fields(window):
    global widgets_sets_count, widgets_set

    if widgets_sets_count >= 12:
        pop_up = tk.Tk()
        pop_up.geometry("155x100")
        pop_up_message = tk.Label(pop_up, text="Maximum components \nreached.")
        pop_up_message.place(x=15, y=30)

        pop_up.resizable(False, False)
        pop_up.mainloop()
        return

    if not widgets_set:
        new_y = 115  # Initial position
    else:
        last_widget_set = widgets_set[-1]
        last_widget = last_widget_set[0]
        last_y = int(last_widget.place_info()['y'])
        new_y = last_y + 27

    combobox_value = tk.StringVar()
    from_entry = tk.Entry(window, bg="#D9D9D9", foreground="#0500FF", font=('Times New Roman', 15, 'bold'))
    to_entry = tk.Entry(window, bg="#D9D9D9", foreground="#0500FF", font=('Times New Roman', 15, 'bold'))
    component_type_combobox = ttk.Combobox(window, textvariable=combobox_value, state='readonly',
                                           values=['R', 'L', 'C', 'Vs', 'Is', 'AC'])
    component_type_combobox.bind("<<ComboboxSelected>>", lambda event: Secondary_Interfaces.set_values_window(window,
                                                                                                              component_type_combobox.get()))

    component_label = tk.Label(window, text=f"{widgets_sets_count + 1}", bg="#D9D9D9",
                               font=('Times New Roman', 15, 'bold'), foreground="#003049")
    remove_button_image = PhotoImage(file=ASSETS_PATH / "frame0\\button_5.png")
    remove_button = Button(image=remove_button_image, borderwidth=0, command=lambda: remove(from_entry, to_entry, component_type_combobox,
                                                                                            remove_button, component_label))
    remove_button.image = remove_button_image  # :)    Keeping a reference to the image for newly created buttons
    # Because only once can an Image be an instance for a button (can't be for multiple buttons)

    from_entry.place(x=105, y=new_y, width=36, height=22)
    to_entry.place(x=180, y=new_y, width=36, height=22)
    component_type_combobox.place(x=250, y=new_y, width=52, height=22)
    remove_button.place(x=369, y=new_y, width=107.0, height=22.0)
    component_label.place(x=60, y=new_y - 2)  # Minor adjustment to y-axis

    widgets_sets_count += 1
    widgets_set.append((from_entry, to_entry, component_type_combobox, remove_button, component_label))


def remove(from_entry, to_entry, type_combobox, remove_button, component_label):
    global widgets_set, widgets_sets_count
    w_index = widgets_set.index((from_entry, to_entry, type_combobox, remove_button, component_label))

    from_entry.destroy()
    to_entry.destroy()
    type_combobox.destroy()
    remove_button.destroy()
    component_label.destroy()
    widgets_set.remove((from_entry, to_entry, type_combobox, remove_button, component_label))
    widgets_sets_count -= 1

    for i in range(w_index, len(widgets_set)):  # Repositioning later instances
        widget_set = widgets_set[i]
        for widget in widget_set:
            place_info = widget.place_info()
            widget.place(x=int(place_info['x']), y=int(place_info['y']) - 27)
        element = widget_set[4].cget("text")
        widget_set[4].configure(text=f"{int(element) - 1}")

    if not widgets_set:
        widgets_sets_count = 0


def clear_all():
    global widgets_set, widgets_sets_count

    for widget_set in widgets_set:
        for widget in widget_set:
            widget.destroy()

    widgets_set = []
    widgets_sets_count = 0
