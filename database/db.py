import sqlite3
from datetime import date

DB_PATH = "meals.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def add_customer(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                   INSERT INTO customers (name, address1, address2, phone, start_date, end_date, default_size, default_special, default_meal_types)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                   (
                       data["name"],
                       data.get("address1", ""),
                       data.get("address2", ""),
                       data.get("phone", ""),
                       data.get("start_date"),
                       data.get("end_date"),
                       data.get("default_size"),
                       data.get("default_special"),
                       data.get("default_meal_types")
                   ))
    customer_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return customer_id

def get_customers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers")
    result = cursor.fetchall()
    conn.close()
    return result

# def get_meals_for_week(customer_id, week_start):

# def update_meal():

# def generate_default_meals_for_week(customer_id, week_start):

