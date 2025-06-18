import sqlite3
import os
from openpyxl import Workbook
from datetime import datetime
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

DB_PATH = "database/meals.db"

# DELIVERY EXPORT 
def export_delivery(date_str):
    os.makedirs("exports", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
                   SELECT
                   c.name,
                   m.size,
                   m.type_special,
                   c.address1,
                   c.address2,
                   c.phone
                   FROM meals m
                   JOIN customers c ON m.customer_id = c.id
                   WHERE m.date = ?
                   ''', (date_str,))
    
    rows = cursor.fetchall()
    conn.close()

    wb = Workbook()
    ws = wb.active
    ws.title = "Delivery"

    export_title = f"{date_str}"
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=6)
    title_cell = ws.cell(row=1, column=1, value=export_title)
    title_cell.font = Font(name="Calibri", size=14, bold=True)
    title_cell.alignment = Alignment(horizontal="center")


    headers = ["Nev", "Meret", "Etkezes + Special", "Cim", "Tel.", "Comment"]
    ws.append(headers)
    header_font = Font(name="Calibri", size=12, bold=True)
    
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=2, column=col_num)
        cell.font = header_font
        cell.fill = PatternFill(start_color="D9D9D9", fill_type="solid")
        cell.alignment = Alignment(horizontal="center")

    fill1 = PatternFill(start_color="FFFFFF", fill_type="solid") # feher
    fill2 = PatternFill(start_color="F2F2F2", fill_type="solid") # light szurke

    for i, row in enumerate(rows, start=3):
        name, size, type_special, addr1, addr2, phone = row
        full_address = f"{addr1} {addr2}".strip()
        values = [name, size, type_special, full_address, phone, ""]

        for j, value in enumerate(values, start=1):
            cell = ws.cell(row=i, column=j, value=value)
            cell.fill = fill1 if i % 2 == 0 else fill2
            cell.alignment = Alignment(vertical="center")


    for row in ws.iter_rows(min_row=3, min_col=2, max_col=2, max_row=ws.max_row):
        for cell in row:
            cell.alignment = Alignment(horizontal="center", vertical="center")

    for row_idx in range(3, ws.max_row + 1):
        ws.row_dimensions[row_idx].height = 20

    for i, col in enumerate(ws.columns, 1):
        max_lenght = 0
        column = get_column_letter(i)
        for cell in col:
            try:
                value_len = len(str(cell.value))
                if value_len > max_lenght:
                    max_lenght = value_len
            except:
                pass


        adjusted_width = max_lenght + 2
        ws.column_dimensions[column].width = adjusted_width

        ws.column_dimensions["F"].width = 30

    filename = f"exports/delivery_{date_str}.xlsx"
    wb.save(filename)

    print(f"[✓] Delivery export completed → {filename}")


