import customtkinter as ctk
from main_menu import MainMenu

if __name__ == "__main__":
    root = ctk.CTk()
    app = MainMenu(root)
    root.mainloop()
