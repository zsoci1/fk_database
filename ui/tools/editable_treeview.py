import tkinter as tk
from tkinter import ttk

# Szerkesztheto treeview a ModPage-be
class EditableTreeView(ttk.Treeview):
    def __init__(self, parent, data, user_id, update_function):
        super().__init__(parent, columns=("datum", "meret", "tipus"), show="headings")

        self.user_id = user_id
        self.update_function = update_function

        # Oszlopok beallitasa
        self.heading("datum", text="Dátum")
        self.heading("meret", text="Méret")
        self.heading("tipus", text="Típus")

        self.column("datum", width=100)
        self.column("meret", width=50)
        self.column("tipus", width=250)

        # Adatok feltoltese
        for row in data:
            self.insert("", "end", values=row)

        # Dupla kattintás esemeny
        self.bind("<Double-1>", self.on_double_click)

        # Szerkesztes entry widget
        self.editing_entry = None

    def on_double_click(self, event):
        region = self.identify("region", event.x, event.y)
        
        if region != "cell":
            return
        
        row_id = self.identify_row(event.y)
        column = self.identify_column(event.x)

        if column != "#3":
            return
        
        x, y, width, height = self.bbox(row_id, column)
        value = self.set(row_id, column)

        if self.editing_entry:
            self.editing_entry.destroy()

        self.editing_entry = tk.Entry(self)
        self.editing_entry.place(x=x, y=y, width=width, height=height)
        self.editing_entry.insert(0, value)
        self.editing_entry.focus_set()

        self.editing_entry.bind("<Return>", lambda e: self.save_edit(row_id, column))
        self.editing_entry.bind("<FocusOut>", lambda e: self.save_edit(row_id, column))

    def save_edit(self, row_id, column):
        new_value = self.editing_entry.get()
        self.editing_entry.destroy()
        self.editing_entry = None
        
        # Eredeti ertekek lekerese (1. oszlop)
        datum = self.set(row_id, "#1")
        
        # Update a tablazatban
        self.set(row_id, column, new_value)
        
        # Frissitjuk a customert
        self.update_function(self.user_id, datum, new_value)