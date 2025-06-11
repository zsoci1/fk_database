import customtkinter as ctk
from tkcalendar import DateEntry

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
        self.date_picker = DateEntry(self, date_pattern='yyyy-mm-dd', width = 13, font=("Arial",14))
        self.date_picker.grid(row =8, column=0, padx=25, pady=10, sticky="w")

        # duration TEXT !
        self.duration_label = ctk.CTkLabel(self, text="Időtartam", font=("Arial", 18))
        self.duration_label.grid(row =9, column =0, padx =20, pady=10, sticky="w")
        self.duration_entry = ctk.CTkEntry(self)
        self.duration_entry.grid(row = 10, column = 0, padx=20, sticky="w")
        
        # Size CTkComboBox !

        # Type CheckBox !

    # error checking

    # dictionarybe rendezes metodus

    # mentes gomb metodus