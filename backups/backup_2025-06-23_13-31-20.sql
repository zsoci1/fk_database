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
INSERT INTO "customers" VALUES(1,'Gita','DS','','092332','2025-06-22',10,'2025-07-02',1,'M','reggeli, ebed, snack, vacsora',0);
INSERT INTO "customers" VALUES(2,'Alfonz','','','','2025-06-22',5,'2025-06-26',0,'XL','reggeli, snack, vacsora',0);
CREATE TABLE meals (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	customer_id INTEGER NOT NULL,
	date DATE NOT NULL,
	size TEXT CHECK(size IN ('S', 'M', 'L', 'XL')),
	type_special TEXT, --vesszovel elvalasztva pl: ebed:vega , snack, vacsora
	price_day INTEGER DEFAULT 0,
	FOREIGN KEY (customer_id) REFERENCES customers(id)
		
);
INSERT INTO "meals" VALUES(1,1,'2025-06-22','S','reggeli, ebed, snack, vacsora',0);
INSERT INTO "meals" VALUES(11,2,'2025-06-22','XL','reggeli, snack, vacsora',0);
INSERT INTO "meals" VALUES(12,2,'2025-06-23','XL','reggeli, snack, vacsora',0);
INSERT INTO "meals" VALUES(13,2,'2025-06-24','XL','reggeli, snack, vacsora',0);
INSERT INTO "meals" VALUES(14,2,'2025-06-25','XL','reggeli, snack, vacsora',0);
INSERT INTO "meals" VALUES(15,2,'2025-06-26','XL','reggeli, snack, vacsora',0);
INSERT INTO "meals" VALUES(25,1,'2025-06-23','M','reggeli, ebed, snack, vacsora',0);
INSERT INTO "meals" VALUES(26,1,'2025-06-24','M','reggeli, ebed, snack, vacsora',0);
INSERT INTO "meals" VALUES(27,1,'2025-06-25','M','reggeli, ebed, snack, vacsora',0);
INSERT INTO "meals" VALUES(28,1,'2025-06-26','M','reggeli, ebed, snack, vacsora',0);
INSERT INTO "meals" VALUES(29,1,'2025-06-26','M','reggeli, ebed, snack, vacsora',0);
INSERT INTO "meals" VALUES(30,1,'2025-06-29','M','reggeli, ebed, snack, vacsora',0);
INSERT INTO "meals" VALUES(31,1,'2025-06-30','M','reggeli, ebed, snack, vacsora',0);
INSERT INTO "meals" VALUES(32,1,'2025-07-01','M','reggeli, ebed, snack, vacsora',0);
INSERT INTO "meals" VALUES(33,1,'2025-07-02','M','reggeli, ebed, snack, vacsora',0);
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('customers',2);
INSERT INTO "sqlite_sequence" VALUES('meals',33);
COMMIT;
