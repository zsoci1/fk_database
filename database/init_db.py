import sqlite3

def initialize_database():
    with open("schema.sql", "r") as f:
        schema = f.read()
    
    conn = sqlite3.connect("meals.db")
    conn.executescript(schema)
    conn.commit()
    conn.close()
    print("Database initialized.")

if __name__ == "__main__":
    initialize_database()