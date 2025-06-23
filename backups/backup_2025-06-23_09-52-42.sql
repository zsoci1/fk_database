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
INSERT INTO "customers" VALUES(1,'Gorinnyo','','','','2025-06-23',20,'2025-07-15',1,'XL','reggeli, ebed, snack, vacsora',25);
CREATE TABLE meals (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	customer_id INTEGER NOT NULL,
	date DATE NOT NULL,
	size TEXT CHECK(size IN ('S', 'M', 'L', 'XL')),
	type_special TEXT, --vesszovel elvalasztva pl: ebed:vega , snack, vacsora
	price_day INTEGER DEFAULT 0,
	FOREIGN KEY (customer_id) REFERENCES customers(id)
		
);
INSERT INTO "meals" VALUES(1,1,'2025-06-23','XL','reggeli, ebed, snack, vacsora',25);
INSERT INTO "meals" VALUES(2,1,'2025-06-24','XL','reggeli, ebed, snack, vacsora',25);
INSERT INTO "meals" VALUES(3,1,'2025-06-25','XL','reggeli, ebed, snack, vacsora',25);
INSERT INTO "meals" VALUES(4,1,'2025-06-26','XL','reggeli, ebed, snack, vacsora',25);
INSERT INTO "meals" VALUES(5,1,'2025-06-26','XL','reggeli, ebed, snack, vacsora (weekend)',25);
INSERT INTO "meals" VALUES(6,1,'2025-06-29','XL','reggeli, ebed, snack, vacsora',25);
INSERT INTO "meals" VALUES(7,1,'2025-06-30','XL','reggeli, ebed, snack, vacsora',25);
INSERT INTO "meals" VALUES(8,1,'2025-07-01','XL','reggeli, ebed, snack, vacsora',25);
INSERT INTO "meals" VALUES(9,1,'2025-07-02','XL','reggeli, ebed, snack, vacsora',25);
INSERT INTO "meals" VALUES(10,1,'2025-07-03','XL','reggeli, ebed, snack, vacsora',25);
INSERT INTO "meals" VALUES(11,1,'2025-07-03','XL','reggeli, ebed, snack, vacsora (weekend)',25);
INSERT INTO "meals" VALUES(12,1,'2025-07-06','XL','reggeli, ebed, snack, vacsora',25);
INSERT INTO "meals" VALUES(13,1,'2025-07-07','XL','reggeli, ebed, snack, vacsora',25);
INSERT INTO "meals" VALUES(14,1,'2025-07-08','XL','reggeli, ebed, snack, vacsora',25);
INSERT INTO "meals" VALUES(15,1,'2025-07-09','XL','reggeli, ebed, snack, vacsora',25);
INSERT INTO "meals" VALUES(16,1,'2025-07-10','XL','reggeli, ebed, snack, vacsora',25);
INSERT INTO "meals" VALUES(17,1,'2025-07-10','XL','reggeli, ebed, snack, vacsora (weekend)',25);
INSERT INTO "meals" VALUES(18,1,'2025-07-13','XL','reggeli, ebed, snack, vacsora',25);
INSERT INTO "meals" VALUES(19,1,'2025-07-14','XL','reggeli, ebed, snack, vacsora',25);
INSERT INTO "meals" VALUES(20,1,'2025-07-15','XL','reggeli, ebed, snack, vacsora',25);
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('customers',1);
INSERT INTO "sqlite_sequence" VALUES('meals',20);
COMMIT;
