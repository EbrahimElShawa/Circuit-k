import tkinter as tk

def create_additional_window(root):
    additional_window = tk.Toplevel(root)

    # Set tool window attribute to hide maximize and minimize buttons
    additional_window.attributes('-toolwindow', 1)

    additional_window.geometry("300x150")
    additional_window.configure(bg="#FFFFFF")

    # Your window content here

    additional_window.resizable(False, False)
    additional_window.mainloop()

# Example usage
root = tk.Tk()
root.geometry("400x200")
root.title("Main Window")

# Call the function from the other file and pass the Tkinter instance
create_additional_window(root)

root.mainloop()
