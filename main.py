import customtkinter as ctk
import tkinter as tk
from tkinter import ttk

# Home page class
class MainMenu(ctk.CTk):
    def __init__(self, master):
        self.master = master
        

# Start
if __name__ == "__main__":
    root = ctk.CTk()
    fitkitchen = MainMenu(root)
    root.mainloop()
