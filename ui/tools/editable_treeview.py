import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
from datetime import datetime

class EditableTreeView(ttk.Treeview):
    def __init__(self, parent, data, user_id, update_function):
        super().__init__(parent, columns=("datum", "meret", "tipus"), show="headings", selectmode="browse")

        self.user_id = user_id
        self.update_function = update_function

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading",
                font=("Verdana", 14, "bold"),
                background="#e1e1e1",
                foreground="#333",
                relief="flat")
        style.map("Treeview", background=[('selected', '#007acc')], foreground=[('selected', 'white')])
        style.configure("Treeview", font=("Verdana", 12))

        self.heading("datum", text="Dátum", anchor="w")
        self.heading("meret", text="Méret", anchor="center")
        self.heading("tipus", text="Típus", anchor="w")

        self.column("meret", anchor="center")


        # Először beszúrjuk az adatokat
        napok = ["Hét", "Kedd", "Sze", "Csüt", "Pén", "Szo", "Vas"]

        for i, row in enumerate(data):
            try:
                date_obj = datetime.strptime(row[0], "%Y-%m-%d")
                nap = napok[date_obj.weekday()]
                formatted_date = f"{nap} ({date_obj.month}.{date_obj.day})"
            except Exception:
                formatted_date = row[0]

            unique_id = f"{row[0]}_{i}"  # <-- Ez biztosítja, hogy minden sor egyedi legyen
            self.insert("", "end", iid=unique_id, values=(formatted_date, row[1], row[2]))
        # Majd dinamikusan beállítjuk az oszlopszélességeket
        self.adjust_column_widths()

        self.bind("<Double-1>", self.on_double_click)

        self.editing_entry = None

    def adjust_column_widths(self):
        font = ("Verdana", 12)
        padding = 27

        columns = self["columns"]
        for idx, col in enumerate(columns):
            header_text = self.heading(col)["text"]
            header_width = tkfont.Font(font=font).measure(header_text)

            max_width = header_width
            for row_id in self.get_children():
                cell_text = self.set(row_id, col)
                cell_width = tkfont.Font(font=font).measure(cell_text)
                if cell_width > max_width:
                    max_width = cell_width

            # Az utolsó oszlop legyen nyújtható (stretch=True)
            stretch = True if idx == len(columns) - 1 else False
            self.column(col, width=max_width + padding, stretch=stretch)


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

        self.editing_entry = tk.Entry(self, font=("Verdana", 11), relief="solid", borderwidth=1)
        self.editing_entry.place(x=x, y=y, width=width, height=height)
        self.editing_entry.insert(0, value)
        self.editing_entry.focus_set()

        self.editing_entry.bind("<Return>", lambda e: self.save_edit(row_id, column))
        self.editing_entry.bind("<FocusOut>", lambda e: self.save_edit(row_id, column))

    def save_edit(self, row_id, column):
        new_value = self.editing_entry.get()
        self.editing_entry.destroy()
        self.editing_entry = None

        self.set(row_id, column, new_value)

        datum = row_id.split("_")[0]  # dátum kiszedése az iid-ből
        self.update_function(self.user_id, datum, new_value)
