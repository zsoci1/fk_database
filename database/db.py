import sqlite3
from datetime import datetime, timedelta

DB_PATH = "database/meals.db"

def get_connection():
    return sqlite3.connect(DB_PATH)


# ───────────────────────────────
# CUSTOMER FUNCTIONS
# ───────────────────────────────

def add_customer(data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO customers (name, address1, address2, phone, start_date, end_date,
                               default_size, default_special, default_meal_types)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
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

    # Generate meals for this customer
    generate_default_meals(customer_id, data["start_date"], data["end_date"], data)

    return customer_id


def get_customers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()
    conn.close()
    return customers


# ───────────────────────────────
# MEAL FUNCTIONS
# ───────────────────────────────

def generate_default_meals(customer_id, start_date, end_date, customer_data):
    """Creates default meals from start_date to end_date for Sun–Thu only"""
    conn = get_connection()
    cursor = conn.cursor()

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    current = start
    while current <= end:
        if current.weekday() in [6, 0, 1, 2, 3]:  # Sun–Thu (0=Mon, 6=Sun)
            cursor.execute("""
                INSERT INTO meals (customer_id, date, size, special, meal_types)
                VALUES (?, ?, ?, ?, ?)
            """, (
                customer_id,
                current.strftime("%Y-%m-%d"),
                customer_data.get("default_size"),
                customer_data.get("default_special"),
                customer_data.get("default_meal_types")
            ))
        current += timedelta(days=1)

    conn.commit()
    conn.close()


def get_meals_for_week(customer_id, week_start_date):
    """Returns all meals for a given week (Sun–Thu) for a customer"""
    conn = get_connection()
    cursor = conn.cursor()

    start = datetime.strptime(week_start_date, "%Y-%m-%d")
    end = start + timedelta(days=4)

    cursor.execute("""
        SELECT date, size, special, meal_types
        FROM meals
        WHERE customer_id = ? AND date BETWEEN ? AND ?
        ORDER BY date ASC
    """, (customer_id, start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")))

    meals = cursor.fetchall()
    conn.close()
    return meals


def update_meal(customer_id, date, new_data): 

    # TODO change to only edit selected data while rest is default
    # TODO add option to halt x number of days and prolong the duration by x number of days


    """Updates a single meal entry"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE meals
        SET size = ?, special = ?, meal_types = ?
        WHERE customer_id = ? AND date = ?
    """, (
        new_data["size"],
        new_data["special"],
        new_data["meal_types"],
        customer_id,
        date
    ))

    conn.commit()
    conn.close()
