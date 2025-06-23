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
INSERT INTO "customers" VALUES(3,'Csicsay Laci','DS','','0290394','2025-06-22',5,'2025-06-26',0,'S','ebed, snack, vacsora',23);
INSERT INTO "customers" VALUES(4,'Tarcsi Krisztina','DS, Karcsai ut','','09234 234','2025-06-22',5,'2025-06-26',1,'S','reggeli, ebed, snack, vacsora',18);
CREATE TABLE meals (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	customer_id INTEGER NOT NULL,
	date DATE NOT NULL,
	size TEXT CHECK(size IN ('S', 'M', 'L', 'XL')),
	type_special TEXT, --vesszovel elvalasztva pl: ebed:vega , snack, vacsora
	price_day INTEGER DEFAULT 0,
	FOREIGN KEY (customer_id) REFERENCES customers(id)
		
);
INSERT INTO "meals" VALUES(13,3,'2025-06-22','S','ebed, snack, vacsora',23);
INSERT INTO "meals" VALUES(14,3,'2025-06-23','S','ebed, snack, vacsora',23);
INSERT INTO "meals" VALUES(15,3,'2025-06-24','S','ebed, snack, vacsora',23);
INSERT INTO "meals" VALUES(16,3,'2025-06-25','S','ebed, snack, vacsora',23);
INSERT INTO "meals" VALUES(17,3,'2025-06-26','S','ebed, snack, vacsora',23);
INSERT INTO "meals" VALUES(18,4,'2025-06-22','S','reggeli, ebed, snack, vacsora',18);
INSERT INTO "meals" VALUES(19,4,'2025-06-23','S','reggeli, ebed, snack, vacsora',18);
INSERT INTO "meals" VALUES(20,4,'2025-06-24','S','reggeli, ebed, snack, vacsora',18);
INSERT INTO "meals" VALUES(21,4,'2025-06-25','S','reggeli, ebed, snack, vacsora',18);
INSERT INTO "meals" VALUES(22,4,'2025-06-26','S','reggeli, ebed, snack, vacsora',18);
INSERT INTO "meals" VALUES(23,4,'2025-06-26','S','reggeli, ebed, snack, vacsora',18);
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('customers',4);
INSERT INTO "sqlite_sequence" VALUES('meals',23);
COMMIT;
