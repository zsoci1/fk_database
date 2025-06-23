import customtkinter as ctk
from ui.main_menu import MainMenu

def run_app():
    root = ctk.CTk()
    app = MainMenu(root)
    root.mainloop()

if __name__ == "__main__":
    run_app()