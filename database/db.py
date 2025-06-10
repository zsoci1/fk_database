import sqlite3

try:

    # connect to DB and create a cursor -> for executing queries
    sqliteConnection = sqlite3.connect('meals.db')
    cursor = sqliteConnection.cursor()
    print("db init")

    # write a query and execute it with a cursor
    # note: queries can be written in form of a string
    query = 'select sqlite_version();'
    cursor.execute(query)

    # fetch and output result
    result = cursor.fetchall()
    print('SQlite version is {}'.format(result))

    # close the cursor
    cursor.close()

# handle errors
except sqlite3.Error as error:
    print('Error occured - ', error)

# close DB connection irrespective of success
# or failure
finally:

    if sqliteConnection:
        sqliteConnection.close()
        print('SQLite connection closed')    

#add customer
    # calculate_end_date() function, 2 parameters: start_date, duration


#get customer


#get meals for day


#update meal