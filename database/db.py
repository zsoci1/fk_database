import sqlite3
from logic.date_tools import calc_end_date

DB_PATH = "database/meals.db"

conn = sqlite3.connect(DB_PATH) # establishing connection to DB
cursor = conn.cursor() # middleman for executing queries

# test dictionary (imagine it's from UI input)
data = {
    "name": "Csicsay Laci",
    "address1": "Ovocny sad",
    "address2": "",
    "phone": "0910 456 543",
    "start_date": "2025-06-11",
    "duration": 20,
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

    

    cursor.execute("""
                   INSERT INTO customers (
                        name, address1, address2, phone, start_date, duration, end_date,
                        default_size, default_type_special
                   )
                   VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
                   """, (
                       name, address1, address2, phone, start_date, duration, end_date,
                       default_size, default_type_special
                   ))
    
    customer_id = cursor.lastrowid # stores the id of the last inserted row
    
    return customer_id



# PRINTING DB (for testing)
def TEST_PRINT():
    add_customer(data)
    result = cursor.execute('''SELECT * FROM customers''')
    for row in result:
        print(row)

# DELETING ALL (for testing)
def DELETE_ALL():
    cursor.execute('''DELETE FROM customers''')


TEST_PRINT()
DELETE_ALL()


conn.commit()
conn.close()



#get customer


#get meals for day


#update meal