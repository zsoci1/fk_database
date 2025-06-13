import customtkinter as ctk

# Home page class
class HomePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_window()

    def setup_window(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weigh=1)
        self.label = ctk.CTkLabel(self, text="Ügyfelek", font=("Arial", 30, "bold"))
        self.label.grid(row = 0, column = 0, padx =20, pady =30, sticky="nw")
