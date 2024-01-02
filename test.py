import tkinter as tk

def hide_main_window():
    root.withdraw()

def show_main_window():
    root.deiconify()

# Create the main window
root = tk.Tk()
root.title("Main Window")

# Create a button to hide the main window
hide_button = tk.Button(root, text="Hide", command=hide_main_window)
hide_button.pack()

# Create a button to show the main window
show_button = tk.Button(root, text="Show", command=show_main_window)
show_button.pack()

# Run the Tkinter event loop
root.mainloop()
