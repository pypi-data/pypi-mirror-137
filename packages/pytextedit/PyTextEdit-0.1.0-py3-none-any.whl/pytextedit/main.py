#!/usr/bin/env python3
# Import
import tkinter as tk
from tkinter import *
import tkinter.filedialog

# Basic stuff i have to do
root = tk.Tk()
root.geometry("720x600")
root.title("PyTextEdit")

# Functions

# Open Function
def open_file():
    filepath = tkinter.filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    ) 
    if not filepath:
        return
    txtedit.delete(1.0, tk.END)
    with open(filepath, "r") as input_file:
        text = input_file.read()
        txtedit.insert(tk.END, text)
    root.title(f"PyTextEdit - {filepath}")

# Save Function
def save_file():
    filepath = tkinter.filedialog.asksaveasfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    with open(filepath, "w") as output_file:
        text = txtedit.get(1.0, tk.END)
        output_file.write(text)
    root.title(f"PyTextEdit - {filepath}")

# Widgets
txtedit = Text(root)
openbtn = Button(root, text = "Open", command = open_file)
savebtn = Button(root, text = "Save As", command = save_file) 



# part 2 of i have to do
openbtn.pack()
savebtn.pack()
txtedit.pack()
root.mainloop()