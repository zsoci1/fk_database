import tkinter as tk
import customtkinter as ctk
from tkcalendar import DateEntry
from database.db import get_customer_defaults

class ChangeDef(ctk.CTkFrame):
    def __init__(self, parent, mainmenu, mod_page):
        super().__init__(parent)
        self.mainmenu = mainmenu
        self.mod_page = mod_page
        self.data = {
            "name":"",
            "address1":"",
            "address2":"",
            "phone":"",
            "weekend_meal":"",
            "default_size":"",
            "default_type_special":"",
            "price_day":""
        }
        self.checkbox_vars=[]
        self.special_entries =[]
        self.meal_data = ["reggeli", "ebed", "snack", "vacsora"]
        self.setup_frame()

        # Nev input
        self.name_label = ctk.CTkLabel(self, text="Név", font=("Arial", 18))
        self.name_label.grid(row =1, column =0, padx =20, pady=10, sticky="w")
        self.name_entry = ctk.CTkEntry(self)
        self.name_entry.grid(row =2, column =0, padx=20, sticky="w")

        # Telefonszam input
        self.phone_label = ctk.CTkLabel(self, text="Telefonszám", font=("Arial", 18))
        self.phone_label.grid(row =1, column =1, padx =20, pady=10, sticky="w")
        self.phone_entry = ctk.CTkEntry(self)
        self.phone_entry.grid(row =2, column =1, padx=20, sticky="w")

        # Cim 1 input
        self.first_address_label = ctk.CTkLabel(self, text="Cím 1", font=("Arial", 18))
        self.first_address_label.grid(row =3, column =0, padx =20, pady=10, sticky="w")
        self.first_address_entry = ctk.CTkEntry(self, placeholder_text="Hétköznap")
        self.first_address_entry.grid(row =4, column =0, padx=20, sticky="w")

        # Cim 2 input
        self.second_address_label = ctk.CTkLabel(self, text="Cím 2", font=("Arial", 18))
        self.second_address_label.grid(row =3, column =1, padx =20, pady=10, sticky="w")
        self.second_address_entry = ctk.CTkEntry(self, placeholder_text="Hétvége")
        self.second_address_entry.grid(row =4, column =1, padx=20, sticky="w")

        # Hetvege input
        self.weekend_checkbox_label = ctk.CTkLabel(self, text="Hétvégi étkezés", font=("Arial", 18))
        self.weekend_checkbox_label.grid(row =5, column =0, padx =20, pady=10, sticky="w")
        self.weekend_var = tk.BooleanVar()
        self.weekend_checkbox = ctk.CTkCheckBox(self, text="", variable=self.weekend_var)
        self.weekend_checkbox.grid(row =6, column = 0, padx=20, sticky="w")
        
        # Meret input
        self.size_label = ctk.CTkLabel(self, text="Méret", font=("Arial", 18))
        self.size_label.grid(row =7, column =0, padx =20, pady=10, sticky="w")
        self.size_combobox = ctk.CTkComboBox(self, values=["S", "M", "L", "XL"], state="readonly")
        self.size_combobox.grid(row=8, column=0, padx=20, pady=(0,10), sticky="w")

        # Price/day input
        self.price_label = ctk.CTkLabel(self, text="Ár/nap", font=("Arial", 18))
        self.price_label.grid(row=9, column=0, padx=20, sticky="w")
        self.price_entry = ctk.CTkEntry(self)
        self.price_entry.grid(row =10, column =0, padx=20, sticky="w")
        
        # Tipus inputok
        self.type_label = ctk.CTkLabel(self, text="Típus", font=("Arial", 18))
        self.type_label.grid(row=7, column=1, padx=20, sticky="w")
        idx = 8
        self.meals = ["Reggeli", "Ebéd", "Snack", "Vacsora"]
        for i,meal in enumerate(self.meals):
            var = tk.BooleanVar()
            self.checkbox = ctk.CTkCheckBox(self, text=meal, variable=var)
            self.checkbox.grid(row=idx, column=1, padx=(20,0), pady=(0,10),sticky="w")
            self.checkbox_vars.append(var)

            entry = ctk.CTkEntry(self)
            entry.grid(row=idx, column=1, padx=(110,0), pady=(0,10), sticky="e")
            self.special_entries.append(entry)
            idx +=1

    # Label and Back button
    def setup_frame(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_rowconfigure(0, weigh=0)

        self.label = ctk.CTkLabel(self, text="Nev", font=("Arial", 30, "bold"))
        self.label.grid(row = 0, column = 0, padx =20, pady =30, sticky="nw")

        from ui.edit_meals import ModPage
        self.back_btn = ctk.CTkButton(self,text="Vissza",command=lambda:self.mainmenu.show_page(ModPage))
        self.back_btn.grid(row=12, column=1, padx=20, sticky="w")

    def load_input(self):
        
        self.chosen_id = self.mod_page.chosen_id
        user_data = get_customer_defaults(self.chosen_id)

        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, user_data["name"])

        self.phone_entry.delete(0, "end")
        self.phone_entry.insert(0, user_data["phone"])

        self.first_address_entry.delete(0,"end")
        self.first_address_entry.insert(0, user_data["address1"])

        self.second_address_entry.delete(0,"end")
        self.second_address_entry.insert(0, user_data["address2"])

        self.second_address_entry.delete(0,"end")
        self.second_address_entry.insert(0, user_data["address2"])

        self.weekend_var.set(False)
        if user_data["weekend_meal"]:
            self.weekend_var.set(True)

        self.size_combobox.set(user_data["default_size"])

        self.price_entry.delete(0, "end")
        self.price_entry.insert(0, user_data["price_day"])

        parsed = self.parse_default_type_special(user_data['default_type_special'])

        for i, meal in enumerate(self.meals):  # self.meals = ["Reggeli", "Ebéd", "Snack", "Vacsora"]
            if parsed[meal] is not None:
                self.checkbox_vars[i].set(True)
            else:
                self.checkbox_vars[i].set(False)

            self.special_entries[i].delete(0, 'end')
            if parsed[meal] not in [None, ""]:
                self.special_entries[i].insert(0, parsed[meal])

        self.save_btn = ctk.CTkButton(self, text="Mentés", command=self.error_handling)
        self.save_btn.grid(row=12,column=0)


    def parse_default_type_special(self,data):
        db_to_display = {
            "reggeli": "Reggeli",
            "ebed": "Ebéd",
            "snack": "Snack",
            "vacsora": "Vacsora"
        }
        # Initialize result with all meals set to None (not selected)
        result = {meal: None for meal in db_to_display.values()}

        if not data:
            return result

        items = [item.strip() for item in data.split(",")]
        for item in items:
            if ':' in item:
                meal, special = item.split(":")
                meal_key = meal.strip().lower()
                if meal_key in db_to_display:
                    result[db_to_display[meal_key]] = special.strip()
            else:
                meal_key = item.strip().lower()
                if meal_key in db_to_display:
                    result[db_to_display[meal_key]] = ""
        return result
    
    def error_handling(self):
        pass

    def update_input(self):
        pass













    


        



