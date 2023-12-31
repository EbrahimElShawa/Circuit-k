import tkinter as tk
from tkinter import Button, PhotoImage, ttk
import Secondary_Interfaces
import circuitTools
import create_files

widgets_sets_count = 0
tip_index = 0
widgets_set = []
ASSETS_PATH = r"./assets/"


def next_tip(canvas, tips, next_button, skip_button):
    global tip_index
    canvas.delete(tips[tip_index])
    if tip_index == 5:
        next_button.destroy()
        skip_button.destroy()
        return
    tip_index += 1
    canvas.itemconfig(tips[tip_index], state="normal")


def skip_tips(canvas, tips, next_button, skip_button):
    for tip in tips:
        canvas.delete(tip)
    next_button.destroy()
    skip_button.destroy()


def add_fields(window, canvas, tips, next_button, skip_button):
    global widgets_sets_count, widgets_set
    skip_tips(canvas, tips, next_button, skip_button)

    if widgets_sets_count >= 12:
        Secondary_Interfaces.pop_up_window(window, "Max Elements Reached")
        return

    if not widgets_set:
        new_y = 115  # Initial position
    else:
        last_widget_set = widgets_set[-1]
        last_widget = last_widget_set[0]
        last_y = int(last_widget.place_info()['y'])
        new_y = last_y + 27

    from_entry = tk.Entry(window, bg="#D9D9D9", foreground="#101010", font=Secondary_Interfaces.active_font)
    to_entry = tk.Entry(window, bg="#D9D9D9", foreground="#101010", font=Secondary_Interfaces.active_font)
    component_type_combobox = ttk.Combobox(window, state='readonly',
                                           values=['R', 'L', 'C', 'Equation', 'Vdc', 'Idc', 'AC'])
    component_label = tk.Label(window, text=f"{widgets_sets_count + 1}", bg="#EEE5DE",
                               font=('Times New Roman', 15, 'bold'), foreground="#003049")
    remove_button_image = PhotoImage(file=ASSETS_PATH + "frame2/button_4.png")
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
        Secondary_Interfaces.pop_up_window(window, "Circuit is empty")
        return

    for i, a in enumerate(widgets_set):
        Secondary_Interfaces.nodes_list[i] = (a[0].get(), a[1].get())

    for value in Secondary_Interfaces.nodes_list:
        if value[0] == '' or value[1] == '':
            Secondary_Interfaces.pop_up_window(window, "Complete Circuit Data")
            return
    for value in Secondary_Interfaces.magnitude_list:
        if value == '':
            Secondary_Interfaces.pop_up_window(window, "Complete Circuit Data")
            return

    for value in Secondary_Interfaces.ramp_time_list:
        if value == '':
            Secondary_Interfaces.pop_up_window(window, "Complete Circuit Data")
            return

    create_files.delete_files()
    create_files.netlist()

    if select == 'Schema':
        circuitTools.picture()
    else:
        if not check():
            Secondary_Interfaces.pop_up_window(window, "Circuit data is not valid")
            return
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


def check():  # check that nodes from 0 to max_node exist and circuit is connected
    from collections import defaultdict
    graph = defaultdict(list)
    max_node = 0
    visited = set()
    for node in Secondary_Interfaces.nodes_list:
        a, b = int(node[0]), int(node[1])
        graph[a].append(b)
        graph[b].append(a)
        max_node = max(max_node, a, b)
    bfs(graph, 0, visited)
    for i in range(max_node + 1):
        if i not in visited:
            return False
    return True


def bfs(graph, start, visited):
    from collections import deque
    queue = deque([start])

    while queue:
        current = queue.popleft()
        if current not in visited:
            print(current)
            visited.add(current)
            queue.extend(neighbor for neighbor in graph[current] if neighbor not in visited)
