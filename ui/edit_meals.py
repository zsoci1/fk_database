import customtkinter as ctk
from database.db import search_customers
from logic.date_tools import get_current_week_range
from database.db import get_meals_for_week
from database.db import update_meal_type
from ui.editable_treeview import EditableTreeView
from CustomTkinterMessagebox import CTkMessagebox

class ModPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_window()
        self.search_bar()
        self.change_default()
        self.change_subscription()
        self.status_subscription()

    def setup_window(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_rowconfigure(0, weigh=0)
        self.label = ctk.CTkLabel(self, text="Módosítás", font=("Arial", 30, "bold"))
        self.label.grid(row = 0, column = 0, padx =20, pady =30, sticky="nw")

    def search_bar(self):
        self.search_entry = ctk.CTkEntry(self, placeholder_text="Keresés...")
        self.search_entry.grid(row =1, column=0, padx=(20,0), pady=10, sticky="w")

        # After every keyrelease, update the suggestions
        self.search_entry.bind("<KeyRelease>", self.update_suggestions)
        self.suggestion_frame = None

    # Get back live query results
    def update_suggestions(self, event=None):
        # Get input from entry
        query = self.search_entry.get().strip()
        
        # If entry is empty
        if query == "":
            # If frame exists, destroy it and set it to none
            if self.suggestion_frame:
                self.suggestion_frame.destroy()
                self.suggestion_frame = None
            return
        
        # if frame doesnt exists, initialize it
        if not self.suggestion_frame:
            self.suggestion_frame = ctk.CTkFrame(self)
            self.suggestion_frame.grid(row=2,column=0,padx=20, sticky="w")
        # else destroy searches
        else:
            for widget in self.suggestion_frame.winfo_children():
                widget.destroy()

        # Search in database
        matches = search_customers(query)

        # If no matches
        if not matches:
            if self.suggestion_frame:
                self.suggestion_frame.destroy()
                self.suggestion_frame = None


        # Format matches and phone numbers
        ids = [id for (id, _, _) in matches]
        names = [name for (_, name, _) in matches]
        phones = [phone for (_, _, phone) in matches]
    
        # Show maximum 5 names
        for i,name in enumerate(names[:5]): 
            btn = ctk.CTkButton(self.suggestion_frame, text=name, 
                                           command=lambda n=name: self.select_customer(n, phones,ids),
                                           fg_color="lightgray", text_color="black", corner_radius=8)
            btn.grid(row=i, column= 0,padx=10, pady=2)

    # When a customer is chosen from suggestions
    def select_customer(self, name, phones, ids):
        self.search_entry.delete(0, 'end')
        self.search_entry.insert(0, name)
        self.chosen_name = name
        self.chosen_number = phones
        self.chosen_id = ids
        self.delete_suggestions()

    # Delete all suggestions
    def delete_suggestions(self):
        if self.suggestion_frame:
            self.suggestion_frame.destroy()
            self.suggestion_frame = None
        self.delete_input(self.search_entry)
        self.show_customer_info()

    # Show chosen customer's info
    def show_customer_info(self):
        if (hasattr(self, 'customer_name_label') and self.customer_name_label.winfo_exists() 
            and hasattr(self, 'customer_phone_label') and self.customer_phone_label.winfo_exists()):
            self.name_label.destroy()
            self.phone_label.destroy()
            self.customer_name_label.destroy()
            self.customer_phone_label.destroy()

        self.name_label = ctk.CTkLabel(self, text='Név:', font=("Arial", 18, "bold"))
        self.name_label.grid(row=2, column=0, padx=(20,0), sticky="w")
        self.customer_name_label = ctk.CTkLabel(self, text=self.chosen_name, font=("Arial", 18))
        self.customer_name_label.grid(row=2, column=0, padx=(65,0), sticky="w")

        self.phone_label = ctk.CTkLabel(self, text='Tel.szám:', font=("Arial", 18, "bold"))
        self.phone_label.grid(row=3, column=0, padx=(20,0), sticky="w")
        self.customer_phone_label = ctk.CTkLabel(self, text=self.chosen_number, font=("Arial", 18))
        self.customer_phone_label.grid(row=3, column=0, padx=(105,0), sticky="w")

        self.load_data()

    # Load data for treeview
    def load_data(self):
        date = get_current_week_range()
        id = self.chosen_id[0]
        meal_for_week = get_meals_for_week(id,date[0], date[1])

        # If treeview exists, destroy it
        if hasattr(self, "editable_treeview"):
            self.editable_treeview.destroy()
        
        # Format date
        formatted_date = "  -  ".join(date)

        # Create label for current work week
        self.week_label = ctk.CTkLabel(self, text=f"Aktuális hét: {formatted_date}", font=("Arial", 18))
        self.week_label.grid(row=9, column=0, padx=20, sticky="w")

        # Then create treeview 
        self.editable_treeview = EditableTreeView(self, meal_for_week, self.chosen_id[0], update_meal_type) 
        self.editable_treeview.grid(row=10, column=0, padx=20, pady=10, sticky="nsew")

    def change_default(self):
        # Error handling -> cannot use this button if no person is selected in search bar
        # CTkMessagebox.messagebox(title='', text='', sound='on', button_text='OK')
        self.change_def_btn = ctk.CTkButton(self, text="Alapértelmezett szerkesztése", font=("Arial", 18))
        self.change_def_btn.grid(row =6, column =0, padx=20, pady=20, sticky="w")

    def status_subscription(self):
        # Error handling -> cannot use this button if no person is selected in search bar
        # CTkMessagebox.messagebox(title='', text='', sound='on', button_text='OK')
        self.change_sub_btn = ctk.CTkButton(self, text="Előfizetés állapota", font=("Arial", 18))
        self.change_sub_btn.grid(row =7, column =0, padx=20, pady=20, sticky="w")

    def change_subscription(self):
        # Error handling -> cannot use this button if no person is selected in search bar
        # CTkMessagebox.messagebox(title='', text='', sound='on', button_text='OK')
        self.change_dur_btn = ctk.CTkButton(self, text="Előfizetés szerkesztése", font=("Arial", 18))
        self.change_dur_btn.grid(row =8, column =0, padx=20, pady=20, sticky="w")
    
    def delete_input(self,input):
        input.delete(0, 'end')