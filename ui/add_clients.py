import customtkinter as ctk
import tkinter as tk
from tkcalendar import DateEntry
import re 
import datetime
from database.db import add_customer
from ui.tools.messsagebox import CustomMessageBox

class AddPage(ctk.CTkFrame):
    def __init__(self, parent, mainmenu):
        super().__init__(parent)
        self.mainmenu = mainmenu
        self.setup_frame()
        self.data = {
            "name":"",
            "address1":"",
            "address2":"",
            "phone":"",
            "start_date":"",
            "duration":"",
            "weekend_meal":"",
            "default_size":"",
            "default_type_special":"",
            "price_day":""
        }
        self.checkbox_vars=[]
        self.special_entries =[]
        self.meal_data = ["reggeli", "ebed", "snack", "vacsora"]
        self.is_correct = False
        self.updated_label = None
        self.user_input()
    
    # Frame beallitasai
    def setup_frame(self):
        for i in range(3):
            self.grid_columnconfigure(i, weight=1, uniform="a")

        for i in range(14):  # vagy amennyi sorod van összesen
            self.grid_rowconfigure(i, weight=0)

        self.grid_rowconfigure(999, weight=1)  # Ez a sor alul "kitölti" az üres helyet
        
        self.label = ctk.CTkLabel(self, text="Hozzáadás", font=("Verdana", 30, "bold"))
        self.label.grid(row = 0, column = 0, padx =20, pady =30, sticky="nw")

    # Input mezok megjelenitese es mentes gomb
    def user_input(self):
        # Nev input
        self.name_label = ctk.CTkLabel(self, text="Név", font=("Verdana", 16))
        self.name_label.grid(row =1, column =0, padx =20, pady=10, sticky="w")
        self.name_entry = ctk.CTkEntry(self)
        self.name_entry.grid(row =2, column =0, padx=20, sticky="ew")

        # Telefonszam input
        self.phone_label = ctk.CTkLabel(self, text="Telefonszám", font=("Verdana", 16))
        self.phone_label.grid(row =1, column =1, padx =20, pady=10, sticky="w")
        self.phone_entry = ctk.CTkEntry(self)
        self.phone_entry.grid(row =2, column =1, padx=20, sticky="ew")

        # Cim 1 input
        self.first_address_label = ctk.CTkLabel(self, text="Cím 1", font=("Verdana", 16))
        self.first_address_label.grid(row =3, column =0, padx =20, pady=10, sticky="w")
        self.first_address_entry = ctk.CTkEntry(self, placeholder_text="Hétköznap (#2 esti címekre)")
        self.first_address_entry.grid(row =4, column =0, padx=20, sticky="ew")

        # Cim 2 input
        self.second_address_label = ctk.CTkLabel(self, text="Cím 2", font=("Verdana", 16))
        self.second_address_label.grid(row =3, column =1, padx =20, pady=10, sticky="w")
        self.second_address_entry = ctk.CTkEntry(self, placeholder_text="Hétvége")
        self.second_address_entry.grid(row =4, column =1, padx=20, sticky="ew")

        # Elofizetes kezdete input
        self.calendar_label = ctk.CTkLabel(self, text="Előfizetés kezdete", font=("Verdana", 16))
        self.calendar_label.grid(row =5, column =0, padx =20, pady=10, sticky="w")
        self.date_picker = DateEntry(self, date_pattern='yyyy-mm-dd', font=("Verdana",14))
        self.date_picker.grid(row =6, column=0, padx=25, pady=10, sticky="ew")

        # Idotartam input
        self.duration_label = ctk.CTkLabel(self, text="Előfizetés időtartama", font=("Verdana", 16))
        self.duration_label.grid(row =5, column =1, padx =20, pady=10, sticky="w")
        self.duration_entry = ctk.CTkEntry(self, placeholder_text="Napok száma")
        self.duration_entry.grid(row =6, column = 1, padx=20, sticky="ew")

        # Hetvege input
        self.weekend_checkbox_label = ctk.CTkLabel(self, text="Hétvégi étkezés", font=("Verdana", 16))
        self.weekend_checkbox_label.grid(row =5, column =2, padx =20, pady=10, sticky="w")
        self.weekend_var = tk.BooleanVar()
        self.weekend_checkbox = ctk.CTkCheckBox(self, text="", variable=self.weekend_var)
        self.weekend_checkbox.grid(row =6, column = 2, padx=20, sticky="w")
        
        
        # Meret input
        self.size_label = ctk.CTkLabel(self, text="Méret", font=("Verdana", 16))
        self.size_label.grid(row =7, column =0, padx =20, pady=10, sticky="w")
        self.size_combobox = ctk.CTkComboBox(self, values=["S", "M", "L", "XL"], state="readonly")
        self.size_combobox.grid(row=8, column=0, padx=20, pady=(0,10), sticky="ew")
        self.size_combobox.set("")

        # Price/day input
        self.price_label = ctk.CTkLabel(self, text="Ár/nap", font=("Verdana", 16))
        self.price_label.grid(row=9, column=0, padx=20, sticky="w")
        self.price_entry = ctk.CTkEntry(self, placeholder_text="€")
        self.price_entry.grid(row =10, column =0, padx=20, sticky="ew")
        
        # Tipus inputok
        self.type_label = ctk.CTkLabel(self, text="Típus", font=("Verdana", 16))
        self.type_label.grid(row=7, column=1, padx=20, sticky="w")
        idx = 8
        self.meals = ["Reggeli", "Ebéd", "Snack", "Vacsora"]
        for i,meal in enumerate(self.meals):
            var = tk.BooleanVar()
            self.checkbox = ctk.CTkCheckBox(self, text=meal, variable=var)
            self.checkbox.grid(row=idx, column=1, padx=(20,0), pady=(0,10),sticky="ew")
            self.checkbox_vars.append(var)

            entry = ctk.CTkEntry(self)
            entry.grid(row=idx, column=1, padx=(110,0), pady=(0,10), sticky="ew")
            self.special_entries.append(entry)
            idx +=1
        

        # Mentes gomb
        self.save_label = ctk.CTkButton(self,text="Mentés", font=("Verdana", 12), command=self.error_handling)
        self.save_label.grid(row=12, column=0, padx=20, pady=(40,0), sticky="ew")

    # Input hiba kezeles popup windowokkal
    def error_handling(self):
        if self.name_entry.get().strip() == "":
            CustomMessageBox(title='Hiba', text='A Név mező nem lehet üres.')
        elif self.date_picker.get().strip() == "":
            CustomMessageBox(title='Hiba', text='Az Előfizetés mező nem lehet üres.')
        elif self.duration_entry.get().strip() == "":
            CustomMessageBox(title='Hiba', text='Az Előfizetés időtartama mező nem lehet üres.')
        elif self.duration_entry.get().strip().isdigit() == False:
            CustomMessageBox(title='Hiba', text='Az Előfizetés időtartamának egy számnak kell lennie.')
            self.delete_input(self.duration_entry)
        elif self.size_combobox.get().strip() == "":
            CustomMessageBox(title='Hiba', text='A Méret mező nem lehet üres.')
        elif self.price_entry.get().strip() =="":
             CustomMessageBox(title='Hiba', text='Az Ár/nap mező nem lehet üres.')
        elif self.price_entry.get().strip().isdigit() == False:
            CustomMessageBox(title='Hiba', text='Az Ár/napnak egy számnak kell lennie.')
        else:
            for var in (self.checkbox_vars):
                checkbox_value = var.get()
                if checkbox_value == True:
                    self.is_correct = True
            if self.is_correct == False:
                CustomMessageBox(title='Hiba', text='A Típus mező nem lehet üres.')
            else:
                # Ha minden elfogadhato, akkor meghvjuk a save_and_reset fuggvenyt
                self.save_and_reset_input()

    # Mentes es input torlese
    def save_and_reset_input(self):
        if self.is_correct == True:
            self.data["name"] = self.name_entry.get()
            self.delete_input(self.name_entry)
            self.data["phone"] = self.phone_entry.get()
            self.delete_input(self.phone_entry)
            self.data["address1"] = self.first_address_entry.get()
            self.delete_input(self.first_address_entry)
            self.data["address2"] = self.second_address_entry.get()
            self.delete_input(self.second_address_entry)
            self.data["start_date"] = self.date_picker.get()
            self.date_picker.set_date(datetime.date.today())
            self.data["duration"] = self.duration_entry.get()
            self.delete_input(self.duration_entry)
            self.data["weekend_meal"] = self.weekend_checkbox.get()
            self.weekend_var.set(False)
            self.data["default_size"] = self.size_combobox.get()
            self.size_combobox.set("")
            self.data["price_day"] = self.price_entry.get()
            self.delete_input(self.price_entry)

            special_data = []
            for meal, var, entry in zip(self.meal_data, self.checkbox_vars, self.special_entries):

                checkbox_value = var.get()
                entry_value = entry.get()

                # Ha a checkbox ki van pipalva
                if checkbox_value == True:
                    # Ha a specialis entry ures
                    if entry_value.strip() == "":
                        special_data.append(meal)
                    else:
                        special_data.append(f"{meal}:{entry_value}")
            # Hozzaadjuk a listat a dict-hez
            self.data["default_type_special"] = ", ".join(special_data)

            # Checkbox es Entry inputok torlese
            for entry in self.special_entries:
                entry.delete(0, 'end')
            for var in self.checkbox_vars:
                var.set(False)

            add_customer(self.data)
            if self.updated_label:
                self.updated_label.destroy()
            self.updated_label = ctk.CTkLabel(self, text="Hozzáadva", font=("Verdana", 14, "bold"), text_color="green")
            self.updated_label.grid(row =13, column=0, padx=20, pady=10, sticky="w")
            self.after(10000, self.updated_label.destroy)

    # Inputok torlese
    def delete_input(self,input):
        input.delete(0, 'end')

