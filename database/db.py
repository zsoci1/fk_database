import sqlite3
from datetime import datetime
from logic.date_tools import calc_end_date, generate_meal_days, get_current_work_week

DB_PATH = "database/meals.db"

# ADD CUSTOMER PANEL 
# megkap egy "data" dictionary-t a UI-bol es elmenti az adatbazisba
def add_customer(data):

    name = data["name"] # returns the value of the name key if exists else error
    address1 = data.get("address1", "") # returns the value but no error if doens't exist
    address2 = data.get("address2", "")
    phone = data.get("phone", "")
    start_date = data["start_date"]
    duration = data["duration"]
    weekend_meal = data["weekend_meal"]
    default_size = data["default_size"]
    default_type_special = data.get("default_type_special", "")
    price_day = int(data.get("price_day", 0))


    end_date = calc_end_date(start_date, duration, weekend_meal_enabled=weekend_meal)

    conn = sqlite3.connect(DB_PATH) # establishing connection to DB
    cursor = conn.cursor() # middleman for executing queries

    cursor.execute('''
                   INSERT INTO customers (
                        name, address1, address2, phone, start_date, duration, end_date,
                        default_size, default_type_special, weekend_meal, price_day
                   )
                   VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ''', (
                       name, address1, address2, phone, start_date, duration, end_date,
                       default_size, default_type_special, weekend_meal, price_day
                   ))
    
    customer_id = cursor.lastrowid # stores the id of the last inserted row
    
    working_days = generate_meal_days(start_date, end_date, weekend_meal_enabled=weekend_meal)


    for meal_info in working_days:
        meal_date = meal_info["date"]
        meal_type = meal_info["type"]

        if meal_type == "weekend":
            type_special = default_type_special + " (weekend)"
        else:
            type_special = default_type_special

        cursor.execute('''
                       INSERT INTO meals (customer_id, date, size, type_special, price_day)
                       VALUES (?, ?, ?, ?, ?)
                       ''', (customer_id, meal_date, default_size, type_special, price_day))


    conn.commit()
    conn.close()

    return customer_id

def search_by_name(customer_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
                   SELECT name
                   FROM customers
                   WHERE id = ?
                   ''', (customer_id,))
    result = cursor.fetchone()

    conn.close()
    return result


# EDIT PANEL, HOME PANEL 
# megkap egy stringet -> query pl "Nev"
# visszaad egy listat minden kozeli talalatrol
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


# EDIT PANEL
# megkapja: customer_id, start_date, end_date
# visszaadja az adott munkahet minden napjat es az azokhoz tartozo meretet es etkezest
# PL egy sor -> 2025.06.12  S  reggeli, ebed, vacsora
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


# EDIT PANEL -> EDIT CUSTOMER DATA 
# megkapja: customer_id
# visszaadja customer default adatait (start date, duration kivetelevel)
def get_customer_defaults(customer_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
                   SELECT name, address1, address2, phone, weekend_meal,
                            default_size, default_type_special, price_day
                   FROM customers
                   WHERE id = ?
                   ''', (customer_id,))
    
    result = cursor.fetchone()
    conn.close()

    if result:
        return {
            "name": result[0],
            "address1": result[1],
            "address2": result[2],
            "phone": result[3],
            "weekend_meal": result[4],
            "default_size": result[5],
            "default_type_special": result[6],
            "price_day": result[7]
        }
    else:
        return None


# EDIT PANEL 
# megkapja: customer_id, date, new_value
# szerkeszti az adott nap etkezeset a type_specialt a meals table-ben
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


# EDIT PANEL -> EDIT CUSTOMER INFO (NEEDS TESTING)
# a default ertekek (pl. nev, cim, tel.) megvaltoztatasara (kiveve start date es duration)
def update_customer_defaults(customer_id, data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
                   UPDATE customers
                   SET name = ?, address1 = ?, address2 = ?, phone = ?, weekend_meal = ?,
                        default_size = ?, default_type_special = ?, price_day = ? 
                   WHERE id = ?
                   ''', (         
                       data["name"],
                       data.get("address1", ""),
                       data.get("address2", ""),
                       data.get("phone", ""),
                       data["weekend_meal"],
                       data["default_size"],
                       data.get("default_type_special", ""),
                       data["price_day"],
                       customer_id
                   ))
    
    today = datetime.today().strftime("%Y-%m-%d")

    cursor.execute('''
                   UPDATE meals
                   SET size = ?, type_special = ?, price_day = ?
                   WHERE customer_id = ?
                   AND date >= ?
                   ''', (
                       data["default_size"],
                       data["default_type_special"],
                       data["price_day"],
                       customer_id,
                       today
                   ))

    conn.commit()
    conn.close()


# EDIT PANEL -> EDIT SUBSCRIPTION & STATE OF SUBSCRIPTION
# megkapja: customer_id 
# visszaad egy dictionary-t ami tartalmazza:  start_date, duration, end_date, remaining days, total sum
def get_subscription_info(customer_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
                   SELECT start_date, duration, end_date, price_day
                   FROM customers
                   WHERE id = ?
                   ''', (customer_id,))
    
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None
    
    start_date, duration, end_date, price_day = row # tuple unpacking

    today = datetime.today().date()
    if end_date:
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
        remaining = max((end_date_obj - today).days + 1, 0)
    else:
        remaining = 0

    total_income = duration * price_day

    return {
        "start_date": start_date,
        "duration": duration,
        "end_date": end_date,
        "remaining_days": remaining,
        "total_income": total_income
    }


# EDIT PANEL -> EDIT SUBSCRIPTION -> STOP SUBSCRIPTION 
# megkapja: customer_id
# atallitja az end_date-et mai napra igy az adatok nem torlodnek de az elofizetes veget er
def stop_subscription(customer_id):
    today = datetime.today().strftime("%Y-%m-%d")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
                   UPDATE customers
                   SET end_date = ?
                   WHERE id = ?
                   ''', (today, customer_id))
    
    cursor.execute('''
                   DELETE FROM meals
                   WHERE customer_id = ?
                   AND date > ?
                   ''', (customer_id, today))

    cursor.execute('''
                   UPDATE customers
                   SET duration = ?
                   WHERE id = ?
                   ''', (0, customer_id))
    conn.commit()
    conn.close()


# EDIT PANEL -> EDIT SUBSCRIPTION -> ACTIVATE SUBSCRIPTION 
def activate_subscription(customer_id, start_date, duration):
    end_date = calc_end_date(start_date, duration)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # update customer with new subscription data
    cursor.execute('''
                   UPDATE customers
                   SET start_date = ?, duration = ?, end_date = ?
                   WHERE id = ?
                   ''', (start_date, duration, end_date, customer_id))
    

    # delete future meals (starting from new start_date)
    cursor.execute('''
                   DELETE FROM meals
                   WHERE customer_id = ?
                   AND date >= ?
                   ''', (customer_id, start_date))
    
    # fetch default values from customers table
    cursor.execute('''
                   SELECT default_size, default_type_special
                   FROM customers
                   WHERE id = ?
                   ''', (customer_id,))

    default_row = cursor.fetchone()

    if default_row:
        default_size, default_type_special = default_row
        working_days = generate_working_day(start_date, end_date)

        for day in working_days:
            cursor.execute('''
                           INSERT INTO meals (customer_id, date, size, type_special)
                           VALUES (?, ?, ?, ?)
                           ''', (customer_id, day, default_size, default_type_special))
            
    conn.commit()
    conn.close()


def extend_subscription(customer_id, extra_days):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
                   SELECT end_date, duration, default_size, default_type_special, weekend_meal, price_day
                   FROM customers
                   WHERE id = ?
                   ''', (customer_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return
    
    end_date, duration, size, type_special, weekend_meal, price_day = row




# PRINTING DB (for testing)
def TEST_PRINT():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("CUSTOMERS TABLE:")
    customer = cursor.execute('''SELECT * FROM customers''')
    for row in customer:
        print(row)
    
    print("MEALS TABLE:")
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

# DELETE_ALL()

TEST_PRINT()

