import sqlite3
from logic.date_tools import calc_end_date, generate_working_day, get_current_work_week

DB_PATH = "database/meals.db"

# test dictionary (imagine it's from UI input)
data = {
    "name": "Teszt Alany",
    "address1": "DS, Ovocny sad",
    "address2": "",
    "phone": "0910 456 543",
    "start_date": "2025-06-08",
    "duration": 5,
    "default_size": "S",
    "default_type_special": "ebed,snack,vacsora"
}

# ADD CUSTOMER PANEL (state -> tested, working)
# add customer
# 'data' is a dictionary filled with user-input from UI 
def add_customer(data):

    name = data["name"] # returns the value of the name key if exists else error
    address1 = data.get("address1", "") # returns the value but no error if doens't exist
    address2 = data.get("address2", "")
    phone = data.get("phone", "")
    start_date = data["start_date"]
    duration = data["duration"]
    end_date = calc_end_date(start_date, duration)
    default_size = data["default_size"]
    default_type_special = data.get("default_type_special", "")

    conn = sqlite3.connect(DB_PATH) # establishing connection to DB
    cursor = conn.cursor() # middleman for executing queries

    cursor.execute('''
                   INSERT INTO customers (
                        name, address1, address2, phone, start_date, duration, end_date,
                        default_size, default_type_special
                   )
                   VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ''', (
                       name, address1, address2, phone, start_date, duration, end_date,
                       default_size, default_type_special
                   ))
    
    customer_id = cursor.lastrowid # stores the id of the last inserted row
    
    working_days = generate_working_day(start_date, end_date)

    # assign default values to every day from start to end date
    for day in working_days:
        cursor.execute('''
                       INSERT INTO meals (customer_id, date, size, type_special)
                       VALUES (?, ?, ?, ?)
                       ''', (
                        customer_id,
                        day,
                        default_size,
                        default_type_special
                       ))

    conn.commit()
    conn.close()

    return customer_id

# EDIT PANEL, HOME PANEL (state -> tested, working)
# takes in a query like : "name", returns a list of closest match in asc order
def search_customers(query):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
                   SELECT id, name, phone
                   FROM customers
                   WHERE name LIKE ? OR phone LIKE ?
                   ORDER BY name ASC
                   ''', (f"%{query}%", f"%{query}%"))
    
    results = cursor.fetchall()
    conn.close()

    return results


# EDIT PANEL (state -> tested, working)
# visszaadja az adott munkahet minden napjat es az azokhoz tartozo meretet es etkezest
# PL 2025.06.12  S  reggeli, ebed, vacsora
def get_meals_for_week(customer_id, start_date, end_date):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
                   SELECT date, size, type_special FROM meals
                   WHERE customer_id = ?
                   AND date BETWEEN ? AND ?
                   ORDER BY date ASC
                   ''', (customer_id, start_date, end_date))
    return cursor.fetchall()


# EDIT PANEL -> EDIT CUSTOMER DATA (state -> under development)
# visszaadja a kivalasztott customer adatait (start date, duration kivetelevel)
def get_customer_defaults(customer_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
                   SELECT name, address1, address2, phone,
                            default_size, default_type_special
                   FROM customers
                   WHERE id = ?
                   ''', (customer_id))
    
    result = cursor.fetchone()
    conn.close()

    if result:
        return {
            "name": result[0],
            "address1": result[1],
            "address2": result[2],
            "phone": result[3],
            "default_size": result[4],
            "default_type_special": result[5]
        }
    else:
        return None





# EDIT PANEL (state -> tested, working)
# szerkeszteni az adott nap etkezeset
def update_meal_type(customer_id, date, new_value):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
                   UPDATE meals
                   SET type_special = ?
                   WHERE customer_id = ? AND date = ?
                   ''', (new_value, customer_id, date))
    conn.commit()
    conn.close()

# PRINTING DB (for testing)
def TEST_PRINT():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("CUSTOMERS TABLE:")
    customer = cursor.execute('''SELECT * FROM customers''')
    for row in customer:
        print(row)
    
    print("MEALS TABLE AZ AKTUALIS HETRE:")
    meals = cursor.execute('''SELECT * FROM meals''')
    for row in meals:
        print(row)
    
# DELETING ALL (for testing)
def DELETE_ALL():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM customers''')
    cursor.execute('''DELETE FROM meals''')
    conn.commit()
    conn.close()

