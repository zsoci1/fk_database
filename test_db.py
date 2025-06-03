from database import db
import sqlite3

def run_tests():
    print("🟢 Starting test sequence...\n")

    # 1. Add a test customer
    test_customer = {
        "name": "Test User",
        "address1": "Street 123",
        "address2": "Apt 4",
        "phone": "123456789",
        "start_date": "2025-06-01",
        "end_date": "2025-06-10",
        "default_size": "L",
        "default_special": "normal",
        "default_meal_types": "reggeli,ebed,vacsora"
    }

    print("➕ Adding test customer...")
    customer_id = db.add_customer(test_customer)
    print(f"✅ Customer added with ID: {customer_id}\n")

    # 2. Fetch and print all customers
    print("📋 All customers:")
    for customer in db.get_customers():
        print(customer)

    # 3. Fetch and print meals for the first week
    print("\n🍽️ Meals for week starting 2025-06-01:")
    meals = db.get_meals_for_week(customer_id, "2025-06-01")
    for meal in meals:
        print(meal)

    # 4. Update a meal
    print("\n✏️ Updating meal on 2025-06-02...")
    db.update_meal(customer_id, "2025-06-02", {
        "size": "M",
        "special": "vegan",
        "meal_types": "ebed"
    })

    # 5. Verify update
    print("🔁 Updated meals:")
    updated_meals = db.get_meals_for_week(customer_id, "2025-06-01")
    for meal in updated_meals:
        print(meal)

    # 6. Clean up test data
    print("\n🧹 Cleaning up test data...")
    delete_test_data(customer_id)
    print("✅ Test data cleaned up.")

def delete_test_data(customer_id):
    conn = sqlite3.connect("database/meals.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM meals WHERE customer_id = ?", (customer_id,))
    cursor.execute("DELETE FROM customers WHERE id = ?", (customer_id,))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    run_tests()
