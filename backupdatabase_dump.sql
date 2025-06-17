BEGIN TRANSACTION;
CREATE TABLE customers (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL,
	address1 TEXT,
	address2 TEXT,
	phone TEXT,
	start_date DATE,
	duration INTEGER NOT NULL,
	end_date DATE,
	weekend_meal INTEGER DEFAULT 0, -- 1 ha aktiv, 0 ha nem
	default_size TEXT CHECK(default_size IN ('S', 'M', 'L', 'XL')),
	default_type_special TEXT, --vesszovel elvalasztva reggeli,ebed-VEGA,..
	price_day INTEGER DEFAULT 0
);
INSERT INTO "customers" VALUES(1,'Pityu','Hello utca','','0923 23 23','2025-06-15',6,'2025-06-19',1,'XL','reggeli, ebed, snack, vacsora',21);
CREATE TABLE meals (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	customer_id INTEGER NOT NULL,
	date DATE NOT NULL,
	size TEXT CHECK(size IN ('S', 'M', 'L', 'XL')),
	type_special TEXT, --vesszovel elvalasztva pl: ebed:vega , snack, vacsora
	price_day INTEGER DEFAULT 0,
	FOREIGN KEY (customer_id) REFERENCES customers(id)
		
);
INSERT INTO "meals" VALUES(1,1,'2025-06-15','XL','reggeli, ebed, snack, vacsora',21);
INSERT INTO "meals" VALUES(2,1,'2025-06-16','XL','reggeli, ebed, snack, vacsora',21);
INSERT INTO "meals" VALUES(3,1,'2025-06-17','XL','reggeli, ebed, snack, vacsora',21);
INSERT INTO "meals" VALUES(4,1,'2025-06-18','XL','reggeli, ebed, snack, vacsora',21);
INSERT INTO "meals" VALUES(5,1,'2025-06-19','XL','reggeli, ebed, snack, vacsora',21);
INSERT INTO "meals" VALUES(6,1,'2025-06-19','XL','reggeli, ebed, snack, vacsora (weekend)',21);
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('customers',1);
INSERT INTO "sqlite_sequence" VALUES('meals',6);
COMMIT;
