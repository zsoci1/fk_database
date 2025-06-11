# this setup file creates the tables inside 'meals.db'
import sqlite3

DB_PATH = "database/meals.db"

with open("schema.sql") as f:
    schema = f.read()

with sqlite3.connect(DB_PATH) as conn:
    conn.executescript(schema)

print("Database created with tables.")
