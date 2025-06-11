import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from tkcalendar import Calendar

# Main menu class
class MainMenu(ctk.CTk):
    # Inicializing methods
    def __init__(self, master):
        self.master = master
        self.current_frame = None
        self.setup_window()
        self.create_widgets()
        self.create_buttons()
        # Default page
        self.show_page(HomePage)

    # Setting up window
    def setup_window(self):
        self.master.title("FitKitchen Manager")
        self.master.geometry("1000x700")
        self.master.resizable(True, True)
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight =1)
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

    # Basic widgets and frames
    def create_widgets(self):
        # Left side navigation bar (buttons)
        self.sidebar_frame = ctk.CTkFrame(self.master)
        self.sidebar_frame.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "ns")

        # Main label in sidebar_frame
        self.main_label = ctk.CTkLabel(self.sidebar_frame, text="FK Manager", font=("Arial", 32, "bold"))
        self.main_label.grid(row = 0, column = 0, padx = 20, pady = 30)

        # Right side content
        self.content_frame = ctk.CTkFrame(self.master)
        self.content_frame.grid(row = 0, column = 1, padx = 20, pady = 20, sticky = "nsew")
        self.content_frame.grid_rowconfigure(0, weight =1) 
        self.content_frame.grid_columnconfigure(0, weight =1)            

    # Creating buttons in sidebar_frame
    def create_buttons(self):   
        self.home_btn = ctk.CTkButton(self.sidebar_frame, text = "Home", font=("Arial", 26, "bold" ), command=lambda:self.show_page(HomePage))
        self.home_btn.grid(row = 1, column = 0, padx = 20, pady = 30)

        self.add_clients_btn = ctk.CTkButton(self.sidebar_frame, text = "Hozzáadás", font=("Arial", 26, "bold" ), command=lambda:self.show_page(AddPage))
        self.add_clients_btn.grid(row = 2, column = 0, padx = 20, pady = 30)

        self.edit_meals_btn = ctk.CTkButton(self.sidebar_frame, text = "Módosítás", font=("Arial", 26, "bold" ), command=lambda:self.show_page(ModPage))
        self.edit_meals_btn.grid(row = 3, column = 0, padx = 20, pady = 30)

        self.exit_btn = ctk.CTkButton(self.sidebar_frame, text = "Kilépés", font=("Arial", 26, "bold" ), command=self.master.destroy)
        self.exit_btn.grid(row = 4, column = 0, padx = 20, pady = 30)

    def show_page(self, page_class):
        # Destroying the current_frame if it exists
        if self.current_frame:
            self.current_frame.destroy()
        # Creating page_class object
        self.current_frame = page_class(self.content_frame)
        self.current_frame.grid(row = 0, sticky = "nsew")

# Home page class
class HomePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_window()

    def setup_window(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weigh=1)
        self.label = ctk.CTkLabel(self, text="Home", font=("Arial", 30, "bold"))
        self.label.grid(row = 0, column = 0, pady = 30, sticky="n")

class AddPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_window()
        self.user_input()

    def setup_window(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_rowconfigure(0, weigh=0)
        self.label = ctk.CTkLabel(self, text="Hozzáadás", font=("Arial", 30, "bold"))
        self.label.grid(row = 0, column = 0, padx =20, pady =30, sticky="n")

    # input metodus
    def user_input(self):
        # name TEXT !
        self.name_label = ctk.CTkLabel(self, text="Név", font=("Arial", 18))
        self.name_label.grid(row =1, column =0, padx =20, pady=10, sticky="w")
        self.name_entry = ctk.CTkEntry(self)
        self.name_entry.grid(row =2, column =0, padx=20, sticky="w")

        # address 1 TEXT
        self.first_address_label = ctk.CTkLabel(self, text="Cím 1", font=("Arial", 18))
        self.first_address_label.grid(row =3, column =0, padx =20, pady=10, sticky="w")
        self.first_address_entry = ctk.CTkEntry(self)
        self.first_address_entry.grid(row =4, column =0, padx=20, sticky="w")

        # address 2 TEXT
        self.second_address_label = ctk.CTkLabel(self, text="Cím 2", font=("Arial", 18))
        self.second_address_label.grid(row =3, column =1, padx =20, pady=10, sticky="w")
        self.second_address_entry = ctk.CTkEntry(self)
        self.second_address_entry.grid(row =4, column =1, padx=20, sticky="w")

        # phone TEXT
        self.phone_label = ctk.CTkLabel(self, text="Telefonszám", font=("Arial", 18))
        self.phone_label.grid(row =5, column =0, padx =20, pady=10, sticky="w")
        self.phone_entry = ctk.CTkEntry(self)
        self.phone_entry.grid(row =6, column =0, padx=20, sticky="w")

        # start date CalendarWidget !
        self.calendar_label = ctk.CTkLabel(self, text="Dátum", font=("Arial", 18))
        self.calendar_label.grid(row =7, column =0, padx =20, pady=10, sticky="w")


        # duration TEXT !

        # Size CTkComboBox !

        # Type CheckBox !

    # error checking

    # dictionarybe rendezes metodus

    # mentes gomb metodus


class ModPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_window()

    def setup_window(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weigh=1)
        self.label = ctk.CTkLabel(self, text="Welcome, this is the Mod page", font=("Arial", 30, "bold"))
        self.label.grid(row = 0, column = 0, pady = 30, sticky="n")

# Start
if __name__ == "__main__":
    root = ctk.CTk()
    # Creating object
    fitkitchen = MainMenu(root)
    root.mainloop()
