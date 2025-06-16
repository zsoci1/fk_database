import customtkinter as ctk

# Home page class
class HomePage(ctk.CTkFrame):
    def __init__(self, parent, mainmenu):
        super().__init__(parent)
        self.mainmenu = mainmenu
        self.setup_frame()

    def setup_frame(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weigh=1)
        self.label = ctk.CTkLabel(self, text="Kimutatás", font=("Arial", 30, "bold"))
        self.label.grid(row = 0, column = 0, padx =20, pady =30, sticky="nw")
