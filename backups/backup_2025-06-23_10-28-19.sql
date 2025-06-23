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
INSERT INTO "customers" VALUES(5,'Tarcsi Krisztina','ds','','092342 23d','2025-06-22',5,'2025-06-26',1,'S','reggeli, ebed, snack, vacsora',12);
INSERT INTO "customers" VALUES(6,'Hetvegi 6 napra','dsi','','090923 44','2025-06-22',6,'2025-06-26',1,'M','reggeli, ebed, snack, vacsora',23);
CREATE TABLE meals (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	customer_id INTEGER NOT NULL,
	date DATE NOT NULL,
	size TEXT CHECK(size IN ('S', 'M', 'L', 'XL')),
	type_special TEXT, --vesszovel elvalasztva pl: ebed:vega , snack, vacsora
	price_day INTEGER DEFAULT 0,
	FOREIGN KEY (customer_id) REFERENCES customers(id)
		
);
INSERT INTO "meals" VALUES(24,5,'2025-06-22','S','reggeli, ebed, snack, vacsora',12);
INSERT INTO "meals" VALUES(25,5,'2025-06-23','S','reggeli, ebed, snack, vacsora',12);
INSERT INTO "meals" VALUES(26,5,'2025-06-24','S','reggeli, ebed, snack, vacsora',12);
INSERT INTO "meals" VALUES(27,5,'2025-06-25','S','reggeli, ebed, snack, vacsora',12);
INSERT INTO "meals" VALUES(28,5,'2025-06-26','S','reggeli, ebed, snack, vacsora',12);
INSERT INTO "meals" VALUES(29,6,'2025-06-22','M','reggeli, ebed, snack, vacsora',23);
INSERT INTO "meals" VALUES(30,6,'2025-06-23','M','reggeli, ebed, snack, vacsora',23);
INSERT INTO "meals" VALUES(31,6,'2025-06-24','M','reggeli, ebed, snack, vacsora',23);
INSERT INTO "meals" VALUES(32,6,'2025-06-25','M','reggeli, ebed, snack, vacsora',23);
INSERT INTO "meals" VALUES(33,6,'2025-06-26','M','reggeli, ebed, snack, vacsora',23);
INSERT INTO "meals" VALUES(34,6,'2025-06-26','M','reggeli, ebed, snack, vacsora',23);
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('customers',6);
INSERT INTO "sqlite_sequence" VALUES('meals',34);
COMMIT;
