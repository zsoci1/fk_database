import sqlite3

# connecting to sqlite
conn = sqlite3.connect('meals.db')

# creating cursor object (for executing queries)
cursor = conn.cursor()

# queries to insert data
cursor.execute('''INSERT INTO customers (name, address1, phone, duration, default_size) VALUES ('Teszt Alany', 'Csillag utca', '0910234567', '20', 'S')''')
cursor.execute('''INSERT INTO customers (name, address1, default_size) VALUES ('Csicsay Laci', 'Ovocny Sad', 'S')''')
cursor.execute('''INSERT INTO customers (name) VALUES ('Suranyi Aranka')''')
cursor.execute('''INSERT INTO customers (name) VALUES ('Varga Pal')''')
print("Data inserted successfully")

data = cursor.execute('''SELECT * FROM customers''')
for row in data:
    print(row)


# DELETING EVERYTHING FROM DATABASE
cursor.execute('''DELETE FROM customers''')
print("DATABASE CLEARED")

# commit changes in the datebase
conn.commit()

# close the connection
conn.close()


#add customer
def add_customer(data):
    name = data["name"]
    address1 = data.get("address1", "")
    address2 = data.get("address2", "")
    phone = data.get("phone", "")
    start_date = data["start_date"]
    duration = data["duration"]
    end_date = # TODO calculate_end_date() function, 2 parameters: start_date, duration
    default_size = data["default_size"]
    default_type_special = data.get("default_type_special", "")


#get customer


#get meals for day


#update meal