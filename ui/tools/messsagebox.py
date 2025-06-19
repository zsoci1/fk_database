import customtkinter as ctk

class CustomMessageBox(ctk.CTkToplevel):
    def __init__(self, master=None, title="Üzenet", text="", width=400, height=150):
        super().__init__(master)
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.resizable(False, False)
        self.grab_set() 
        
        # Szöveg megjelenítése (word-wrap)
        self.label = ctk.CTkLabel(self, text=text,font=("Verdana", 12), wraplength=width - 40, justify="left")
        self.label.pack(padx=20, pady=(20, 10), fill="both", expand=True)
        
        # OK gomb
        self.ok_button = ctk.CTkButton(self, text="OK",font=("Verdana", 10), command=self.destroy)
        self.ok_button.pack(pady=(0, 20))
        
        # Ablak középre helyezése a főablakhoz képest
        self.center_window()

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