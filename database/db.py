import sqlite3
from logic.date_tools import calc_end_date, generate_working_day

DB_PATH = "database/meals.db"

conn = sqlite3.connect(DB_PATH) # establishing connection to DB
cursor = conn.cursor() # middleman for executing queries

# test dictionary (imagine it's from UI input)
data = {
    "name": "Csicsay Laci",
    "address1": "Ovocny sad",
    "address2": "",
    "phone": "0910 456 543",
    "start_date": "2025-06-08",
    "duration": 5,
    "default_size": "S",
    "default_type_special": "ebed,snack,vacsora"
}

# add customer
# 'data' is a dictionary filled with user-input from UI 
def add_customer(data):
    name = data["name"] # returns the value of the name key if exists else error
    address1 = data.get("address1", "") # returns the value but no error if doens't exist
    address2 = data.get("address2", "")
    phone = data.get("phone", "")
    start_date = data["start_date"]
    duration = data["duration"]
    end_date = calc_end_date(start_date, duration) # calculate_end_date() function, 2 parameters: start_date, duration
    default_size = data["default_size"]
    default_type_special = data.get("default_type_special", "")

    

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
    
    working_day = generate_working_day(start_date, end_date)

    # assign default values to every day from start to end date
    for day in working_day:
        cursor.execute('''
                       INSERT INTO meals (customer_id, date, size, type_special)
                       VALUES (?, ?, ?, ?)
                       ''', (
                        customer_id,
                        day,
                        default_size,
                        default_type_special
                       ))


    return customer_id



# PRINTING DB (for testing)
def TEST_PRINT():
    add_customer(data)

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
    cursor.execute('''DELETE FROM customers''')
    cursor.execute('''DELETE FROM meals''')


TEST_PRINT()
DELETE_ALL()
conn.commit()
conn.close()


#get customer


#get meals for day


#update meal