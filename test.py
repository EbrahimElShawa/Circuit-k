import tkinter as tk

def open_toplevel():
    # Create a Toplevel window
    toplevel = tk.Toplevel(root)
    toplevel.title("Toplevel Window")

    # Button to destroy the Toplevel window
    destroy_button = tk.Button(toplevel, text="Destroy Toplevel", command=toplevel.destroy)
    destroy_button.pack()

    # Release the grab when the Toplevel window is destroyed
    toplevel.protocol("WM_DELETE_WINDOW", lambda: release_grab(root))

    # Set the grab to the Toplevel window
    toplevel.grab_set()

def release_grab(parent):
    # Release the grab when the Toplevel window is destroyed
    parent.grab_release()

# Create the Tkinter window
root = tk.Tk()

# Button to open the Toplevel window
open_button = tk.Button(root, text="Open Toplevel", command=open_toplevel)
open_button.pack()

# Run the Tkinter event loop
root.mainloop()
