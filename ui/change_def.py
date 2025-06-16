import tkinter as tk
import customtkinter as ctk
from tkcalendar import DateEntry


class ChangeDef(ctk.CTkFrame):
    def __init__(self, parent, mainmenu):
        super().__init__(parent)
        self.mainmenu = mainmenu
        self.data = {
            "name":"",
            "address1":"",
            "address2":"",
            "phone":"",
            "start_date":"",
            "duration":"",
            "default_size":"",
            "default_type_special":""
        }
        self.checkbox_vars=[]
        self.special_entries =[]
        self.meal_data = ["reggeli", "ebed", "snack", "vacsora"]

        self.setup_frame()

    # Label and Back button
    def setup_frame(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_rowconfigure(0, weigh=0)

        self.label = ctk.CTkLabel(self, text="Megrendelő", font=("Arial", 30, "bold"))
        self.label.grid(row = 0, column = 0, padx =20, pady =30, sticky="nw")

        from ui.edit_meals import ModPage
        self.back_btn = ctk.CTkButton(self,text="Vissza",command=lambda:self.mainmenu.show_page(ModPage))
        self.back_btn.grid(row=12, column=0, padx=20, sticky="w")

