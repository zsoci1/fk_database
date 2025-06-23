import tkinter as tk
import customtkinter as ctk
from tkcalendar import DateEntry
from datetime import datetime, date
from database.db import get_customer_defaults
from database.db import update_customer_defaults
from database.db import get_subscription_info
from database.db import stop_subscription
from database.db import extend_subscription
from database.db import pause_subscription
from ui.tools.messsagebox import CustomMessageBox
from ui.activate_subs import ActivateSubs

class ChangeDef(ctk.CTkScrollableFrame):
    def __init__(self, parent, mainmenu, mod_page):
        super().__init__(parent)
        self.mainmenu = mainmenu
        self.mod_page = mod_page

        # Data loading
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

        # Setting None for later checking
        self.updated_label = None
        self.save_btn = None
        self.pause_subscription = None
        self.start_subscription = None
        self.start_date = None
        self.end_date = None
        self.duration = None
        self.days_left = None
        self.total_sum = None

        self.setup_frame()

        # INPUT FIELDS

        # Name input
        self.name_label = ctk.CTkLabel(self, text="Név", font=("Verdana", 16))
        self.name_label.grid(row =1, column =0, padx =20, pady=10, sticky="w")
        self.name_entry = ctk.CTkEntry(self)
        self.name_entry.grid(row =2, column =0, padx=20, sticky="ew")

        # Phone input
        self.phone_label = ctk.CTkLabel(self, text="Telefonszám", font=("Verdana", 16))
        self.phone_label.grid(row =1, column =1, padx =20, pady=10, sticky="w")
        self.phone_entry = ctk.CTkEntry(self)
        self.phone_entry.grid(row =2, column =1, padx=20, sticky="ew")

        # Address 1 input
        self.first_address_label = ctk.CTkLabel(self, text="Cím 1", font=("Verdana", 16))
        self.first_address_label.grid(row =3, column =0, padx =20, pady=10, sticky="w")
        self.first_address_entry = ctk.CTkEntry(self, placeholder_text="Hétköznap")
        self.first_address_entry.grid(row =4, column =0, padx=20, sticky="ew")

        # Address 2 input
        self.second_address_label = ctk.CTkLabel(self, text="Cím 2", font=("Verdana", 16))
        self.second_address_label.grid(row =3, column =1, padx =20, pady=10, sticky="w")
        self.second_address_entry = ctk.CTkEntry(self, placeholder_text="Hétvége")
        self.second_address_entry.grid(row =4, column =1, padx=20, sticky="ew")

        # Weekend meal input
        self.weekend_checkbox_label = ctk.CTkLabel(self, text="Hétvégi étkezés", font=("Verdana", 16))
        self.weekend_checkbox_label.grid(row =5, column =0, padx =20, pady=10, sticky="w")
        self.weekend_var = tk.BooleanVar()
        self.weekend_checkbox = ctk.CTkCheckBox(self, text="", variable=self.weekend_var)
        self.weekend_checkbox.grid(row =6, column = 0, padx=20, sticky="w")
        
        # Size input
        self.size_label = ctk.CTkLabel(self, text="Méret", font=("Verdana", 16))
        self.size_label.grid(row =7, column =0, padx =20, pady=10, sticky="w")
        self.size_combobox = ctk.CTkComboBox(self, values=["S", "M", "L", "XL"], state="readonly")
        self.size_combobox.grid(row=8, column=0, padx=20, pady=(0,10), sticky="ew")

        # Price/day input
        self.price_label = ctk.CTkLabel(self, text="Ár/nap", font=("Verdana", 16))
        self.price_label.grid(row=9, column=0, padx=20, sticky="w")
        self.price_entry = ctk.CTkEntry(self)
        self.price_entry.grid(row =10, column =0, padx=20, sticky="ew")
        
        # Type / Type Special inputs
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

        # SUBSCRIPTION LABELS

        # Start subscription
        self.start_date_label = ctk.CTkLabel(self, text="Kezdete: ", font=("Verdana", 16))
        self.start_date_label.grid(row =13, column=0, padx=(20,0), sticky="w")

        # End subscription
        self.end_date_label = ctk.CTkLabel(self, text="Vége: ", font=("Verdana", 16))
        self.end_date_label.grid(row=14, column=0, padx=(20,0), sticky="w")

        # Duration
        self.duration_label = ctk.CTkLabel(self, text="Időtartam: ", font=("Verdana", 16))
        self.duration_label.grid(row=15, column=0, padx=(20,0), sticky="w")

        # Remaining days
        self.days_left_label = ctk.CTkLabel(self, text="Hátralévő napok: ", font=("Verdana", 16))
        self.days_left_label.grid(row=16, column=0, padx=(20,0), sticky="w")

        # Total sum
        self.total_sum_label = ctk.CTkLabel(self, text="Teljes összeg: ", font=("Verdana", 16))
        self.total_sum_label.grid(row=17, column=0, padx=(20,0), sticky="w")

        # SUBSCRIPTION ENTRIES AND LABELS

        # Extend by value
        self.extend_sub_label = ctk.CTkLabel(self, text="Meghosszabbítás", font=("Verdana", 16))
        self.extend_sub_label.grid(row=19, column=0, padx=(20,0), pady=10, sticky="w")
        self.extend_sub_entry = ctk.CTkEntry(self, width=50)
        self.extend_sub_entry.grid(row=19,column=0, padx=(170,0), sticky="w")
        self.extend_sub_label_2 = ctk.CTkLabel(self, text="nappal", font=("Verdana", 16))
        self.extend_sub_label_2.grid(row=19, column=0, padx=(230,0), sticky="w")

        # Stop subscription label
        self.stop_label = ctk.CTkLabel(self, text="Leállítás kezdete és vége", font=("Verdana", 16))
        self.stop_label.grid(row=20, column=0, padx=20, sticky="w")

        # Stop subscription start date entry
        self.pause_start = DateEntry(self, date_pattern='yyyy-mm-dd', width = 13, font=("Verdana",14))
        self.pause_start.grid(row =21, column=0, pady=10,padx=25, sticky="w")
        self.pause_start.delete(0, 'end')

        # Stop subscription end date entry
        self.pause_end = DateEntry(self, date_pattern='yyyy-mm-dd', width = 13, font=("Verdana",14))
        self.pause_end.grid(row =21, column=0, padx=(200,0), pady=10, sticky="w")
        self.pause_end.delete(0, 'end')

        # Delete subscription date inputs button
        self.delete_button = ctk.CTkButton(self, text="x", font=("Verdana",8,"bold"), width=50, command=lambda:self.delete_date_inputs())
        self.delete_button.grid(row =21, column=0, padx=(305,0), sticky="w")

    # Deleting subscription date inputs
    def delete_date_inputs(self):
        self.pause_start.delete(0, 'end')
        self.pause_end.delete(0, 'end')


    # Labels and Back button
    def setup_frame(self):
        self.grid_rowconfigure(0, weight=0)
        for i in range(2):
            self.grid_columnconfigure(i, weight=1, uniform="a")

        self.label = ctk.CTkLabel(self, text="Adatok szerkesztése", font=("Verdana", 20, "bold"))
        self.label.grid(row = 0, column =0, padx =20, pady =20, sticky="nw")

        self.subscription_status_label = ctk.CTkLabel(self, text="Előfizetés állapota", font=("Verdana", 20, "bold"))
        self.subscription_status_label.grid(row =12, column = 0, padx =20, pady =20, sticky="nw")

        self.subscription_label = ctk.CTkLabel(self, text="Előfizetés szerkesztése", font=("Verdana", 20,"bold"))
        self.subscription_label.grid(row =18, column = 0, padx =20, pady =20, sticky="nw")

        from ui.edit_meals import ModPage
        self.back_btn = ctk.CTkButton(self,text="Vissza",font=("Verdana", 12),command=lambda:self.mainmenu.show_page(ModPage))
        self.back_btn.grid(row=24, column=0, padx=20, pady=40, sticky="w")

    # Update/Load all data
    def load_input(self):
        self.delete_date_inputs()
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

        if self.save_btn is None:
            self.save_btn = ctk.CTkButton(self, text="Mentés",font=("Verdana", 12),command=self.error_handling)
            self.save_btn.grid(row=24,column=1, padx=20, pady=40, sticky="w")
        self.show_subscription()

    # Type special separation logic
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
    
    # Error handling for inputs
    def error_handling(self):
        # Checking entry dates
        self.is_correct = False
        self.today = date.today().isoformat()
        if self.pause_start.get() != "" and self.pause_end.get() != "":
            # Converting them 
            start_date_str = self.pause_start.get()
            end_date_str = self.pause_end.get()
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

        # Checking input fields
        if self.name_entry.get().strip() == "":
            CustomMessageBox(title='Hiba', text='A Név mező nem lehet üres.')
        elif self.size_combobox.get().strip() == "":
            CustomMessageBox(title='Hiba', text='A Méret mező nem lehet üres.')
        elif self.price_entry.get().strip() =="":
             CustomMessageBox(title='Hiba', text='Az Ár/nap mező nem lehet üres.')
        elif self.price_entry.get().strip().isdigit() == False:
            CustomMessageBox(title='Hiba', text='Az Ár/napnak egy számnak kell lennie.')
        elif self.extend_sub_entry.get().strip() != "" and self.extend_sub_entry.get().strip().isdigit() == False:
            CustomMessageBox(title='Hiba', text='Az Előfizetés meghosszabbítása mezőnek egy számnak kell lennie.')
        elif self.pause_start.get() != "" and self.pause_end.get() != "" and start_date > end_date:
            CustomMessageBox(title='Hiba', text='A leállítás vége nem lehet hamarabb mint a leállítás kezdete.')
        elif self.pause_start.get() != "" and self.pause_end.get() != "" and start_date_str < self.today:
            CustomMessageBox(title='Hiba', text='A leállítás kezdete dátum nem lehet a múltban.')
        else:
            for var in (self.checkbox_vars):
                checkbox_value = var.get()
                if checkbox_value == True:
                    self.is_correct = True
            if self.is_correct == False:
                CustomMessageBox(title='Hiba', text='A Típus mező nem lehet üres.')
            # If no error happened
            else:
                # Extend subscription if needed
                if self.extend_sub_entry.get().strip() !="":
                    extend_subscription(self.chosen_id,int(self.extend_sub_entry.get().strip()))
                    self.extend_sub_entry.delete(0,"end")
                # Pause subscription if needed
                if self.pause_start.get() != "" and self.pause_end.get() != "":
                    pause_subscription(self.chosen_id,self.pause_start.get(),self.pause_end.get())
                # Save the data, and delete date inputs
                self.save_data()
                self.delete_date_inputs()

    # Saving all data
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

                if checkbox_value == True:
                    if entry_value.strip() == "":
                        special_data.append(meal)
                    else:
                        special_data.append(f"{meal}:{entry_value}")

            # Add special_data to user_data dictionary
            self.user_data["default_type_special"] = ", ".join(special_data)

            # Update the customer's default settings in DB
            update_customer_defaults(self.chosen_id,self.user_data)
            # Refresh the ModPage
            self.mod_page.refresh_page()

            # Updated successfully label
            if self.updated_label:
                self.updated_label.destroy()
            self.updated_label = ctk.CTkLabel(self, text="Mentve", font=("Verdana", 12, "bold"), text_color="green")
            self.updated_label.grid(row =24, column=1, padx=20, pady=(0,60),sticky="w")
            self.after(5000, self.updated_label.destroy)
            self.show_subscription()

    # Show subscription info
    def show_subscription(self):
        self.data = get_subscription_info(self.chosen_id)

        if self.start_date is None:
            self.start_date = ctk.CTkLabel(self, text=self.data["start_date"], font=("Verdana", 16, "bold"))
            self.start_date.grid(row =13, column=0, padx=(180,0), sticky="w")
        else:
            self.start_date.configure(text=self.data["start_date"])
        
        if self.end_date is None:
            self.end_date = ctk.CTkLabel(self, text=self.data["end_date"], font=("Verdana", 16, "bold"))
            self.end_date.grid(row =14, column=0, padx=(180,0), sticky="w")
        else:
            self.end_date.configure(text=self.data["end_date"])

        if self.duration is None:
            self.duration =ctk.CTkLabel(self, text=self.data["duration"], font=("Verdana", 16, "bold"))
            self.duration.grid(row=15, column=0,padx=(180,0), sticky="w")
        else:
            self.duration.configure(text=self.data["duration"])

        if self.days_left is None:
            self.days_left =ctk.CTkLabel(self, text=self.data["remaining_days"], font=("Verdana", 16, "bold"))
            self.days_left.grid(row=16, column=0,padx=(180,0), sticky="w")
        else:
            self.days_left.configure(text=self.data["remaining_days"])

        if self.total_sum is None:
            self.total_sum = ctk.CTkLabel(self, text=f"{self.data["total_income"]}€", font=("Verdana", 16, "bold"))
            self.total_sum.grid(row=17, column=0, padx=(180,0), sticky="w")
        else:
            self.total_sum.configure(text=f"{self.data["total_income"]}€")

        self.subscription_buttons()

    # Show subscription buttons
    def subscription_buttons(self):
        if self.pause_subscription is None:
            self.pause_subscription = ctk.CTkButton(self, text="Előfizetés leállítása\n(mai naptól)",font=("Verdana", 16), width=200, command=self.stop_subs)
            self.pause_subscription.grid(row=22, column=0, padx=20, pady=10, sticky="w")

        if self.start_subscription is None:
            self.start_subscription = ctk.CTkButton(self, text="Előfizetés aktiválása ⧉",font=("Verdana", 16), command=self.activate_subscription) 
            self.start_subscription.grid(row=23, column=0, padx=20, pady=10, sticky="w")

    # Stop the subscription
    def stop_subs(self):
        stop_subscription(self.chosen_id)
        self.show_subscription()
        self.mod_page.refresh_page()
        if self.updated_label:
            self.updated_label.destroy()
        self.updated_label = ctk.CTkLabel(self, text="Mentve", font=("Verdana", 12, "bold"), text_color="green")
        self.updated_label.grid(row =24, column=1, padx=20, pady=(0,60),sticky="w")
        self.after(5000, self.updated_label.destroy)

    # Create TopLevel for activate subscription
    def activate_subscription(self):
        today = date.today().isoformat()
        end = self.data["end_date"]  
        if end > today:  
            # if customer is active
            CustomMessageBox(title='Hiba', text='A megrendelő már aktív.')
        else:
            # if customer is not active
            if not hasattr(self, "activate_window") or not self.activate_window.winfo_exists():
                self.activate_window = ActivateSubs(self,self.chosen_id, self.weekend_checkbox.get(),self.mod_page)
            else:
                self.activate_window.focus()















    


        



