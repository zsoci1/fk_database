# IF UPDATING SCHEMA DURING DEVELOPMENT
import sqlite3

DB_PATH = "database/meals.db"

with open("database/schema.sql", "r") as f:
    schema = f.read()

with sqlite3.connect(DB_PATH) as conn:
    conn.executescript("""
    DROP TABLE IF EXISTS meals;
    DROP TABLE IF EXISTS customers;
    """) 
    conn.executescript(schema)

print("Database reset and created from schema.sql")
