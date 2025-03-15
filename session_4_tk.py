import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Hello, World! - Tkinter")
root.geometry("300x200")  # Set window size

# Create a label
label = tk.Label(root, text="Hello, World!", font=("Arial", 20))
label.pack(pady=50)  # Center the label with some padding

# Run the Tkinter event loop
root.mainloop()
