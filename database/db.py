import sqlite3

# connecting to sqlite
conn = sqlite3.connect('meals.db')

# creating cursor object (for executing queries)
cursor = conn.cursor()

# queries to insert data
cursor.execute('''INSERT INTO customers (name, address1) VALUES ('Teszt Alany', 'Csillag utca')''')
cursor.execute('''INSERT INTO customers (name) VALUES ('Csicsay Laci')''')
cursor.execute('''INSERT INTO customers (name) VALUES ('Suranyi Aranka')''')
cursor.execute('''INSERT INTO customers (name) VALUES ('Varga Pal')''')
print("Data inserted successfully")

data = cursor.execute('''SELECT * FROM customers''')
for row in data:
    print(row)

# commit changes in the datebase
conn.commit()

# close the connection
conn.close()








#add customer
    # calculate_end_date() function, 2 parameters: start_date, duration


#get customer


#get meals for day


#update meal