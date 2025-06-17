import tkinter as tk
import customtkinter as ctk
from tkcalendar import DateEntry
from database.db import get_customer_defaults
from database.db import update_customer_defaults
from database.db import get_subscription_info
from database.db import stop_subscription
from database.db import activate_subscription
from ui.tools.messsagebox import CustomMessageBox

class ChangeDef(ctk.CTkScrollableFrame):
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
        self.is_correct = False
        self.updated_label = None
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

        # Elofizetes kezdete
        self.start_date_label = ctk.CTkLabel(self, text="Kezdete: ", font=("Arial", 18))
        self.start_date_label.grid(row =13, column=0, padx=(20,0), sticky="w")

        # Elofizetes vege
        self.end_date_label = ctk.CTkLabel(self, text="Vége: ", font=("Arial", 18))
        self.end_date_label.grid(row=14, column=0, padx=(20,0), sticky="w")

        # Idotartam
        self.duration_label = ctk.CTkLabel(self, text="Időtartam: ", font=("Arial", 18))
        self.duration_label.grid(row=15, column=0, padx=(20,0), sticky="w")

        # Hatralevo napok
        self.days_left_label = ctk.CTkLabel(self, text="Hátralévő napok: ", font=("Arial", 18))
        self.days_left_label.grid(row=16, column=0, padx=(20,0), sticky="w")

        # Teljes osszeg
        self.total_sum_label = ctk.CTkLabel(self, text="Teljes összeg: ", font=("Arial", 18))
        self.total_sum_label.grid(row=17, column=0, padx=(20,0), sticky="w")

        # Meghosszabbitas x nappal
        self.extend_sub_label = ctk.CTkLabel(self, text="Meghosszabbítás", font=("Arial", 18))
        self.extend_sub_label.grid(row=19, column=0, padx=(20,0), sticky="w")
        self.extend_sub_entry = ctk.CTkEntry(self, width=50)
        self.extend_sub_entry.grid(row=19,column=0, padx=(170,0), sticky="w")
        self.extend_sub_label_2 = ctk.CTkLabel(self, text="nappal", font=("Arial", 18))
        self.extend_sub_label_2.grid(row=19, column=0, padx=(240,0), sticky="w")

        # Leallitas
        self.stop_label = ctk.CTkLabel(self, text="Leállítás", font=("Arial", 18))
        self.stop_label.grid(row=20, column=0, padx=(20,0), sticky="w")

        # Leallitas kezdete entry
        self.pause_start = DateEntry(self, date_pattern='yyyy-mm-dd', width = 13, font=("Arial",14))
        self.pause_start.grid(row =20, column=0, padx=(160,0), pady=10, sticky="w")

        # Leallitas vege entry
        self.pause_end = DateEntry(self, date_pattern='yyyy-mm-dd', width = 13, font=("Arial",14))
        self.pause_end.grid(row =20, column=0, padx=(360,0), pady=10, sticky="w")


    # Label and Back button
    def setup_frame(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_rowconfigure(0, weigh=0)

        self.label = ctk.CTkLabel(self, text="Adatok szerkesztése", font=("Arial", 30, "bold"))
        self.label.grid(row = 0, column =0, padx =20, pady =30, sticky="nw")

        self.subscription_status_label = ctk.CTkLabel(self, text="Előfizetés állapota", font=("Arial", 30, "bold"))
        self.subscription_status_label.grid(row =12, column = 0, padx =20, pady =30, sticky="nw")

        self.subscription_label = ctk.CTkLabel(self, text="Előfizetés szerkesztése", font=("Arial", 30, "bold"))
        self.subscription_label.grid(row =18, column = 0, padx =20, pady =30, sticky="nw")

        from ui.edit_meals import ModPage
        self.back_btn = ctk.CTkButton(self,text="Vissza",command=lambda:self.mainmenu.show_page(ModPage))
        self.back_btn.grid(row=23, column=0, padx=20, pady=20, sticky="w")

    def load_input(self):
        
        self.chosen_id = self.mod_page.chosen_id
        self.user_data = get_customer_defaults(self.chosen_id)

        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, self.user_data["name"])

        self.phone_entry.delete(0, "end")
        self.phone_entry.insert(0, self.user_data["phone"])

        self.first_address_entry.delete(0,"end")
        self.first_address_entry.insert(0, self.user_data["address1"])

        self.second_address_entry.delete(0,"end")
        self.second_address_entry.insert(0, self.user_data["address2"])

        self.second_address_entry.delete(0,"end")
        self.second_address_entry.insert(0, self.user_data["address2"])

        self.weekend_var.set(False)
        if self.user_data["weekend_meal"]:
            self.weekend_var.set(True)

        self.size_combobox.set(self.user_data["default_size"])

        self.price_entry.delete(0, "end")
        self.price_entry.insert(0, self.user_data["price_day"])

        parsed = self.parse_default_type_special(self.user_data['default_type_special'])

        for i, meal in enumerate(self.meals):  
            if parsed[meal] is not None:
                self.checkbox_vars[i].set(True)
            else:
                self.checkbox_vars[i].set(False)

            self.special_entries[i].delete(0, 'end')
            if parsed[meal] not in [None, ""]:
                self.special_entries[i].insert(0, parsed[meal])

        # Load extend
        # Load pause start
        # Load pause end

        #self.save_btn = ctk.CTkButton(self, text="Mentés", command=self.error_handling)
        #self.save_btn.grid(row=12,column=0, padx=20, sticky="w")

        self.show_subscription()


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
        if self.name_entry.get().strip() == "":
            CustomMessageBox(title='Hiba', text='A Név mező nem lehet üres.')
        elif self.size_combobox.get().strip() == "":
            CustomMessageBox(title='Hiba', text='A Méret mező nem lehet üres.')
        elif self.price_entry.get().strip() =="":
             CustomMessageBox(title='Hiba', text='Az Ár/nap mező nem lehet üres.')
        elif self.price_entry.get().strip().isdigit() == False:
            CustomMessageBox(title='Hiba', text='Az Ár/napnak egy számnak kell lennie.')
        # check extend, check pause start, check pause end
        else:
            for var in (self.checkbox_vars):
                checkbox_value = var.get()
                if checkbox_value == True:
                    self.is_correct = True
            if self.is_correct == False:
                CustomMessageBox(title='Hiba', text='A Típus mező nem lehet üres.')
            else:
                # Ha minden elfogadhato, akkor meghvjuk a save_and_reset fuggvenyt
                self.save_data()

    def save_data(self):
        if self.is_correct == True:
            self.user_data["name"] = self.name_entry.get()
            self.user_data["phone"] = self.phone_entry.get()
            self.user_data["address1"] = self.first_address_entry.get()
            self.user_data["address2"] = self.second_address_entry.get()
            self.user_data["weekend_meal"] = self.weekend_checkbox.get()
            self.user_data["default_size"] = self.size_combobox.get()
            self.user_data["price_day"] = self.price_entry.get()

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
            self.user_data["default_type_special"] = ", ".join(special_data)

            update_customer_defaults(self.chosen_id,self.user_data)
            self.mod_page.refresh_page()

            #if self.updated_label:
                #self.updated_label.destroy()
            #self.updated_label = ctk.CTkLabel(self, text="Sikeresen frissítve", font=("Arial", 18, "bold"), text_color="green")
            #self.updated_label.grid(row =13, column=0, padx=20, pady=20, sticky="w")
            #self.after(10000, self.updated_label.destroy)

    def show_subscription(self):
        data = get_subscription_info(self.chosen_id)
        print(data)

        # DESTROY BEFORE CREATING AGAIN !!!!!
        self.start_date = ctk.CTkLabel(self, text=data["start_date"], font=("Arial", 18, "bold"))
        self.start_date.grid(row =13, column=0, padx=(180,0), sticky="w")

        self.end_date = ctk.CTkLabel(self, text=data["end_date"], font=("Arial", 18, "bold"))
        self.end_date.grid(row =14, column=0, padx=(180,0), sticky="w")

        self.duration =ctk.CTkLabel(self, text=data["duration"], font=("Arial", 18, "bold"))
        self.duration.grid(row=15, column=0,padx=(180,0), sticky="w")

        self.days_left =ctk.CTkLabel(self, text=data["remaining_days"], font=("Arial", 18, "bold"))
        self.days_left.grid(row=16, column=0,padx=(180,0), sticky="w")

        self.total_sum = ctk.CTkLabel(self, text=f"{data["total_income"]}€", font=("Arial", 18, "bold"))
        self.total_sum.grid(row=17, column=0, padx=(180,0), sticky="w")

        self.subscription_buttons()

    def subscription_buttons(self):
        # Elofizetes leallitasa gomb
        self.pause_subscription = ctk.CTkButton(self, text="Előfizetés leállítása (mai naptól)",font=("Arial", 18), command=stop_subscription(self.chosen_id))
        self.pause_subscription.grid(row=21, column=0, padx=20, pady=10, sticky="w")

        # Elofizetes aktivalasa gomb
        self.start_subscription = ctk.CTkButton(self, text="Előfizetés aktiválása",font=("Arial", 18)) # Command uj page
        self.start_subscription.grid(row=22, column=0, padx=20, pady=10, sticky="w")

    def update_subscription(self):
        pass













    


        



