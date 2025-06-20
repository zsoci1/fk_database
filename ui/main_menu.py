import customtkinter as ctk
import tkinter as tk
from ui.add_clients import AddPage
from ui.edit_meals import ModPage
from ui.change_def import ChangeDef
from ui.export import ExportPage

# Main menu class
class MainMenu(ctk.CTk):
    # Inicializing methods
    def __init__(self, master):
        self.master = master
        self.current_frame = None
        
        self.setup_window()
        self.create_widgets()
        # Load all pages into a dictionary
        self.pages = {}
        self.pages[AddPage] = AddPage(self.content_frame, self)
        self.pages[ExportPage] = ExportPage(self.content_frame, self)
        # Create ModPage first
        mod_page = ModPage(self.content_frame, self)
        self.pages[ModPage] = mod_page
        # Now we can safely pass mod_page to ChangeDef
        self.pages[ChangeDef] = ChangeDef(self.content_frame, self, mod_page)
        for page in self.pages.values():    
            page.grid(row=0, column=0, sticky="nsew")
            page.grid_remove()
        self.create_buttons()
        # Show efault page
        self.show_page(ExportPage)

    # Setting up window
    def setup_window(self):
        self.master.title("FitKitchen Manager")
        self.master.geometry("1000x700")
        self.master.resizable(True, True)
        self.master.minsize(1000, 600)
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight =1)  

        # Desired window size
        width = 1000
        height = 700

        # Get screen dimensions
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # Calculate position
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))

        # Apply size and position
        self.master.geometry(f"{width}x{height}+{x}+{y}")

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

    # Basic widgets and frames
    def create_widgets(self):
        # Left side navigation bar (buttons)
        self.sidebar_frame = ctk.CTkFrame(self.master, fg_color="#CFCFCF")
        self.sidebar_frame.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "ns")

        # Main label in sidebar_frame
        self.main_label = ctk.CTkLabel(self.sidebar_frame, text="FK Manager", font=("Verdana", 32, "bold"))
        self.main_label.grid(row = 0, column = 0, padx = 20, pady = 30)

        # Right side content
        self.content_frame = ctk.CTkFrame(self.master)
        self.content_frame.grid(row = 0, column = 1, padx = 20, pady = 20, sticky = "nsew")
        self.content_frame.grid_rowconfigure(0, weight =1) 
        self.content_frame.grid_columnconfigure(0, weight =1)            

    # Creating buttons in sidebar_frame
    def create_buttons(self):   

        self.export_btn = ctk.CTkButton(self.sidebar_frame, text ="Exportálás", font=("Verdana", 22, "bold" ), width=130, height=38, command=lambda:self.show_page(ExportPage))
        self.export_btn.grid(row =1, column =0, padx =20, pady =35)

        self.add_clients_btn = ctk.CTkButton(self.sidebar_frame, text ="Hozzáadás", font=("Verdana", 22, "bold" ),width=130,height=38, command=lambda:self.show_page(AddPage))
        self.add_clients_btn.grid(row =2, column =0, padx =20, pady =35)

        self.edit_meals_btn = ctk.CTkButton(self.sidebar_frame, text ="Módosítás", font=("Verdana", 22, "bold" ),width=130,height=38, command=lambda:self.show_page(ModPage))
        self.edit_meals_btn.grid(row =3, column =0, padx =20, pady =35)

        self.exit_btn = ctk.CTkButton(self.sidebar_frame, text ="Kilépés", font=("Verdana", 22, "bold" ),width=140,height=38, command=self.master.destroy)
        self.exit_btn.grid(row =4, column =0, padx =20, pady =35)

    def show_page(self, page_name):
        # Load user_input data before showing ChangeDef
        if page_name == ChangeDef:
            self.pages[ChangeDef].load_input()

        # Hiding the current_frame if it exists
        if self.current_frame:
            self.current_frame.grid_remove()
        # Creating page_class object
        self.current_frame = self.pages[page_name]
        self.current_frame.grid()