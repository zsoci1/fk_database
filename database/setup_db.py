# this setup file creates the tables inside 'meals.db'
import sqlite3

with open("database/schema.sql") as f:
    schema = f.read()

with sqlite3.connect("database/meals.db") as conn:
    conn.executescript(schema)

print("Database created with tables.")
