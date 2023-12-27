import tkinter as tk


def open_toplevel():
    # Create a new Toplevel window
    toplevel = tk.Toplevel(root)

    # Set the title and geometry of the Toplevel window
    toplevel.title("Toplevel Window")
    toplevel.geometry("300x200")

    # Create a button in the Toplevel window
    close_button = tk.Button(toplevel, text="Close Toplevel", command=lambda: close_toplevel(toplevel))
    close_button.pack(pady=20)


def close_toplevel(toplevel):
    # Close the Toplevel window
    toplevel.destroy()

    # Focus back on the main Tkinter window
    root.deiconify()


# Create the main Tkinter window
root = tk.Tk()

# Create a button in the main window to open the Toplevel window
open_button = tk.Button(root, text="Open Toplevel", command=open_toplevel)
open_button.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
