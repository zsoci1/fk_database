import customtkinter as ctk
import tkinter as tk
import os
from ui.main_menu import MainMenu

if __name__ == "__main__":
    root = ctk.CTk()
    app = MainMenu(root)
    root.mainloop()
