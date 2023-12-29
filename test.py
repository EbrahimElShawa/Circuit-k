import tkinter as tk

def on_entry_focus_out(event):
    # Get the value of the Entry widget when it loses focus
    entry_value = entry.get()
    print(f"Entry value on focus out: {entry_value}")

# Create the main window
root = tk.Tk()
root.title("Entry Example")

# Create an Entry widget
entry = tk.Entry(root)
entry2 = tk.Entry(root)
entry.pack(padx=10, pady=10)
entry2.pack(padx=20, pady=20)

# Bind the function to the FocusOut event of the Entry
entry.bind("<FocusOut>", on_entry_focus_out)

# Start the main loop
root.mainloop()
