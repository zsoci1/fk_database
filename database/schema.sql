-- Customers table
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address1 TEXT,
    address2 TEXT,
    phone TEXT,
    start_date DATE,
    end_date DATE,
    default_size TEXT CHECK(default_size IN ('S', 'M', 'L', 'XL')),
    default_special TEXT,
    default_meal_types TEXT -- comma-separated 'reggeli,ebed,vacsora'
);

-- Meals table
CREATE TABLE IF NOT EXISTS meals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    date DATE NOT NULL,
    size TEXT CHECK(size IN ('S', 'M', 'L', 'XL')),
    special TEXT,
    meal_types TEXT, -- comma-separated 'reggeli,vacsora'
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);
