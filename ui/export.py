import customtkinter as ctk
from tkcalendar import DateEntry
from datetime import date, timedelta
from ui.tools.messsagebox import CustomMessageBox
from logic.export import export_delivery
from logic.export import export_kitchen

class ExportPage(ctk.CTkFrame):
    def __init__(self, parent, mainmenu):
        super().__init__(parent)
        self.mainmenu = mainmenu
        self.setup_frame()
        self.create_widgets()

    # Label
    def setup_frame(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weigh=0)
        self.label = ctk.CTkLabel(self, text="Exportálás", font=("Arial", 30, "bold"))
        self.label.grid(row = 0, column = 0, padx =20, pady =30, sticky="nw")

    # Create all widgets
    def create_widgets(self):
        # Date label
        self.date_label = ctk.CTkLabel(self, text="Dátum", font=("Arial", 18))
        self.date_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        
        # Date picker
        self.date_picker = DateEntry(self, date_pattern='yyyy-mm-dd', width = 13, font=("Arial",14))
        self.date_picker.grid(row=2, column=0, padx=25, pady=10, sticky="w")
        self.tomorrow = (date.today() + timedelta(days=1)).isoformat()
        self.date_picker.set_date(self.tomorrow)

        self.delivery_export_btn = ctk.CTkButton(self, text="Futár EXPORT", command=self.exp_del)
        self.delivery_export_btn.grid(row=3, column=0, padx=20, pady=10, sticky="w")

        self.cook_export_btn = ctk.CTkButton(self, text="Szakács EXPORT", command=self.exp_kit)
        self.cook_export_btn.grid(row=4, column=0, padx=20, pady=10, sticky="w")

        self.all_export_btn = ctk.CTkButton(self, text="Minden EXPORT", command=self.exp_all)
        self.all_export_btn.grid(row=5, column=0, padx=20, pady=10, sticky="w")

        self.location_label = ctk.CTkLabel(self, text=f"Mentés helye: ...\\exports\\{self.date_picker.get().strip()}.xlsx")
        self.location_label.grid(row=6,column=0, padx=20, pady=10, sticky="w")
    
    def exp_del(self):
        if self.date_picker.get().strip() =="":
            CustomMessageBox(title='Hiba', text='A Dátum mező nem lehet üres.')
        else:
            export_delivery(self.date_picker.get().strip())
            if self.date_picker.get().strip() != self.tomorrow:
                self.location_label.destroy()
                self.location_label = ctk.CTkLabel(self, text=f"Mentés helye: ...\\exports\\{self.date_picker.get().strip()}.xlsx")
                self.location_label.grid(row=6,column=0, padx=20, pady=10, sticky="w")

    def exp_kit(self):
        if self.date_picker.get().strip() =="":
                CustomMessageBox(title='Hiba', text='A Dátum mező nem lehet üres.')
        else:
            export_kitchen(self.date_picker.get().strip())
            if self.date_picker.get().strip() != self.tomorrow:
                self.location_label.destroy()
                self.location_label = ctk.CTkLabel(self, text=f"Mentés helye: ...\\exports\\{self.date_picker.get().strip()}.xlsx")
                self.location_label.grid(row=6,column=0, padx=20, pady=10, sticky="w")

    def exp_all(self):
        if self.date_picker.get().strip() =="":
                CustomMessageBox(title='Hiba', text='A Dátum mező nem lehet üres.')
        else:
            export_delivery(self.date_picker.get().strip())
            export_kitchen(self.date_picker.get().strip())
            if self.date_picker.get().strip() != self.tomorrow:
                self.location_label.destroy()
                self.location_label = ctk.CTkLabel(self, text=f"Mentés helye: ...\\exports\\{self.date_picker.get().strip()}.xlsx")
                self.location_label.grid(row=6,column=0, padx=20, pady=10, sticky="w")
    





