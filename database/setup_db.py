# run this every time there is a change to the schema
# this setup file creates the tables inside 'meals.db'
import sqlite3

with open("schema.sql") as f:
    schema = f.read()

with sqlite3.connect("meals.db") as conn:
    conn.executescript(schema)

print("Database created with tables.")
