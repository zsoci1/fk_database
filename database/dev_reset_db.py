# UPDATING SCHEMA DURING DEVELOPMENT
import sqlite3

with open("schema.sql", "r") as f:
    schema = f.read()

with sqlite3.connect("meals.db") as conn:
    conn.executescript("""
    DROP TABLE IF EXISTS meals;
    DROP TABLE IF EXISTS customers;
    """) 
    conn.executescript(schema)

print("Database reset and created from schema.sql")
