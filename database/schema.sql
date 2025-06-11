CREATE TABLE IF NOT EXISTS customers (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL,
	adress1 TEXT,
	adress2 TEXT,
	phone TEXT,
	start_date DATE,
	duration INTEGER NOT NULL,
	end_date DATE,
	default_size TEXT CHECK(default_size IN ('S', 'M', 'L', 'XL')),
	default_type_special TEXT --vesszovel elvalasztva reggeli,ebed-VEGA,..
);

CREATE TABLE IF NOT EXISTS meals (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	customer_id INTEGER NOT NULL,
	date DATE NOT NULL,
	size TEXT CHECK(size IN ('S', 'M', 'L', 'XL')),
	type_special TEXT, --vesszovel elvalasztva pl: ebed VEGA, snack, vacsora
	FOREIGN KEY (customer_id) REFERENCES customers(id)
);
