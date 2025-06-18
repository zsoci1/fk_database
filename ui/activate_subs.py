import customtkinter as ctk
from tkcalendar import DateEntry
from database.db import activate_subscription

class ActivateSubs(ctk.CTkToplevel):
    def __init__(self, parent, id, weekend):
        super().__init__(parent)
        self.setup_window()
        self.center_window()
        self.setup_window()
        self.empty_error = None
        self.notdigit_error = None
        self.id = id
        self.weekend = weekend
        self.parent = parent
        self.grab_set()
        self.user_input()

    def setup_window(self):
        self.title("Előfizetés aktiválása")
        self.geometry("400x200")
    
    def user_input(self):
        self.start_date_label = ctk.CTkLabel(self, text="Kezdés", font=("Arial", 18))
        self.start_date_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.start_date = DateEntry(self, date_pattern='yyyy-mm-dd', width =13, font=("Arial",14))
        self.start_date.grid(row=0, column=1, padx=0, pady=10, sticky="w")

        self.duration_label = ctk.CTkLabel(self, text="Időtartam", font=("Arial", 18))
        self.duration_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.duration = ctk.CTkEntry(self)
        self.duration.grid(row=1, column=1, padx=0, pady=10, sticky="w")

        self.save_btn = ctk.CTkButton(self, text="Mentés", command=self.error_handling)
        self.save_btn.grid(row=3, column=1, padx=20, pady=10)

    def center_window(self):
        self.update_idletasks()
        if self.master:
            master_x = self.master.winfo_rootx()
            master_y = self.master.winfo_rooty()
            master_w = self.master.winfo_width()
            master_h = self.master.winfo_height()
            win_w = self.winfo_width()
            win_h = self.winfo_height()
            pos_x = master_x + (master_w - win_w) // 2
            pos_y = master_y + (master_h - win_h) // 2
            self.geometry(f"+{pos_x}+{pos_y}")
        else:
            # Ha nincs master, akkor a képernyő közepére
            screen_w = self.winfo_screenwidth()
            screen_h = self.winfo_screenheight()
            win_w = self.winfo_width()
            win_h = self.winfo_height()
            pos_x = (screen_w - win_w) // 2
            pos_y = (screen_h - win_h) // 2
            self.geometry(f"+{pos_x}+{pos_y}")

    def error_handling(self):
        if self.duration.get().strip() == "":
            if self.empty_error:
                self.empty_error.destroy()
            if self.notdigit_error:
                self.notdigit_error.destroy()
            self.empty_error = ctk.CTkLabel(self, text="Az Időtartam mező nem lehet üres.", font=("Arial", 14), text_color="red")
            self.empty_error.grid(row=2, column=1, padx=0, sticky="w")
        elif self.duration.get().strip().isdigit() == False:
            if self.empty_error:
                self.empty_error.destroy()
            if self.notdigit_error:
                self.notdigit_error.destroy()
            self.notdigit_error = ctk.CTkLabel(self, text="Az Időtartam mezőnek\negy számnak kell lennie.", font=("Arial", 14), text_color="red")
            self.notdigit_error.grid(row=2, column=1, padx=0, sticky="w")
        else:
            if self.notdigit_error:
                self.notdigit_error.destroy()
            if self.empty_error:
                self.empty_error.destroy()
            activate_subscription(self.id, self.start_date.get().strip(), self.duration.get().strip(), self.weekend)
            self.parent.show_subscription()
            self.destroy()
