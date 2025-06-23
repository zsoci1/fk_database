import customtkinter as ctk
from database.db import search_customers
from logic.date_tools import get_current_week_range
from database.db import get_meals_for_week
from database.db import update_meal_type
from database.db import search_by_name
from ui.tools.editable_treeview import EditableTreeView
from ui.tools.messsagebox import CustomMessageBox
from ui.change_def import ChangeDef

class ModPage(ctk.CTkFrame):
    def __init__(self, parent, mainmenu):
        super().__init__(parent)
        self.mainmenu = mainmenu
        self.change_def_btn = None
        self.whisper_btn = None
        self.week_label = None
        self.setup_frame()
        self.search_bar()

    def setup_frame(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_rowconfigure(0, weigh=0)
        self.label = ctk.CTkLabel(self, text="Módosítás", font=("Verdana", 30, "bold"))
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
        
        # Show maximum 5 names
        for i,(id_, name, phone)in enumerate(matches[:5]): 
            btn = ctk.CTkButton(self.suggestion_frame, text=name, 
                                           command=lambda n=name, p=phone, id_val=id_: self.select_customer(n, p, id_val),
                                           fg_color="lightgray", text_color="black", corner_radius=8)
            btn.grid(row=i, column= 0,padx=10, pady=2)

    # When a customer is chosen from suggestions
    def select_customer(self, name, phone, id):
        self.search_entry.delete(0, 'end')
        self.search_entry.insert(0, name)
        self.chosen_name = name
        self.chosen_number = phone
        self.chosen_id = id
        self.mainmenu.chosen_name = self.chosen_name
        self.mainmenu.chosen_id = self.chosen_id
        self.delete_suggestions()

    # Delete all suggestions
    def delete_suggestions(self):
        if self.suggestion_frame:
            self.suggestion_frame.destroy()
            self.suggestion_frame = None
        self.delete_input(self.search_entry)
        self.load_data()

    # Show chosen customer's info
    def show_customer_info(self):
        if (hasattr(self, 'customer_name_label') and self.customer_name_label.winfo_exists() 
            and hasattr(self, 'customer_phone_label') and self.customer_phone_label.winfo_exists()):
            self.customer_name_label.destroy()
            self.customer_phone_label.destroy()
            self.name_label.destroy()
            self.phone_label.destroy()

        name_and_phone = search_by_name(self.chosen_id)
        
        self.name_label = ctk.CTkLabel(self, text='Név:', font=("Verdana", 18, "bold"))
        self.name_label.grid(row=2, column=0, padx=(20,0), sticky="w")
        self.customer_name_label = ctk.CTkLabel(self, text=name_and_phone[0], font=("Verdana", 18))
        self.customer_name_label.grid(row=2, column=0, padx=(70,0), sticky="w")

        self.phone_label = ctk.CTkLabel(self, text='Tel.szám:', font=("Verdana", 18, "bold"))
        self.phone_label.grid(row=3, column=0, padx=(20,0), sticky="w")
        self.customer_phone_label = ctk.CTkLabel(self, text=name_and_phone[1], font=("Verdana", 18))
        self.customer_phone_label.grid(row=3, column=0, padx=(120,0), sticky="w")

        self.change_default()

    # Load data for treeview
    def load_data(self):

        date = get_current_week_range()
        id = self.chosen_id
        meal_for_week = get_meals_for_week(id,date[0], date[1])

        # If treeview exists, destroy it
        if hasattr(self, "editable_treeview"):
            self.editable_treeview.destroy()
        
        # Format date
        formatted_date = "  -  ".join(date)

        # Create label for current work week
        if self.week_label is None:
            self.week_label = ctk.CTkLabel(self, text=f"Aktuális hét: {formatted_date}", font=("Verdana", 18))
            self.week_label.grid(row=9, column=0, padx=20, sticky="w")

        # Whisper button for correct input
        if self.whisper_btn is None:
            self.whisper_btn = ctk.CTkButton(self, text="Súgó", font=("Verdana", 12),command=lambda:CustomMessageBox(
            title='Súgó',
            text='Típus mező használata:\n❌ reggeli vega tejmentes, ebed vega...\n✔️ reggeli:vega tejmentes, ebed:vega...',    
            ))
            self.whisper_btn.grid(row=10, column=0, padx=20, pady=10, sticky="w")

        # Create treeview
        self.editable_treeview = EditableTreeView(self, meal_for_week, self.chosen_id, update_meal_type) 
        self.editable_treeview.grid(row=11, column=0, padx=20, pady=10, sticky="nsew")

        self.show_customer_info()

    def change_default(self):
        if self.change_def_btn is None:
            self.change_def_btn = ctk.CTkButton(self, text="Megrendelő adatainak szerkesztése", font=("Verdana", 18), command=lambda: self.mainmenu.show_page(ChangeDef))
            self.change_def_btn.grid(row =6, column =0, padx=20, pady=20, sticky="w")
    
    def delete_input(self,input):
        input.delete(0, 'end')

    def refresh_page(self):
        self.load_data()