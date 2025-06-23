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
INSERT INTO "customers" VALUES(1,'Gita','DS','','092332','2025-06-22',16,'2025-07-13',1,'M','reggeli, ebed, snack, vacsora',0);
INSERT INTO "customers" VALUES(2,'Alfonz','','','','2025-06-22',5,'2025-06-26',0,'XL','reggeli, snack, vacsora',0);
INSERT INTO "customers" VALUES(3,'Rebeka','','','','2025-06-23',10,'2025-07-09',0,'M','reggeli, ebed, snack, vacsora',0);
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
INSERT INTO "meals" VALUES(107,1,'2025-06-25','M','reggeli, ebed, snack, vacsora',0);
INSERT INTO "meals" VALUES(108,1,'2025-06-26','M','reggeli, ebed, snack, vacsora',0);
INSERT INTO "meals" VALUES(109,1,'2025-06-26','M','reggeli, ebed, snack, vacsora',0);
INSERT INTO "meals" VALUES(110,1,'2025-06-29','M','reggeli, ebed, snack, vacsora',0);
INSERT INTO "meals" VALUES(111,1,'2025-06-30','M','reggeli, ebed, snack, vacsora',0);
INSERT INTO "meals" VALUES(112,1,'2025-07-01','M','reggeli, ebed, snack, vacsora',0);
INSERT INTO "meals" VALUES(113,1,'2025-07-02','M','reggeli, ebed, snack, vacsora',0);
INSERT INTO "meals" VALUES(114,1,'2025-07-03','M','reggeli, ebed, snack, vacsora',0);
INSERT INTO "meals" VALUES(115,1,'2025-07-03','M','reggeli, ebed, snack, vacsora',0);
INSERT INTO "meals" VALUES(116,1,'2025-07-06','M','reggeli, ebed, snack, vacsora',0);
INSERT INTO "meals" VALUES(117,1,'2025-07-07','M','reggeli, ebed, snack, vacsora',0);
INSERT INTO "meals" VALUES(118,1,'2025-07-08','M','reggeli, ebed, snack, vacsora',0);
INSERT INTO "meals" VALUES(119,1,'2025-07-09','M','reggeli, ebed, snack, vacsora',0);
INSERT INTO "meals" VALUES(120,1,'2025-07-10','M','reggeli, ebed, snack, vacsora',0);
INSERT INTO "meals" VALUES(157,3,'2025-06-26','M','reggeli, ebed, snack, vacsora',0);
INSERT INTO "meals" VALUES(158,3,'2025-06-29','M','reggeli, ebed, snack, vacsora',0);
INSERT INTO "meals" VALUES(159,3,'2025-06-30','M','reggeli, ebed, snack, vacsora',0);
INSERT INTO "meals" VALUES(160,3,'2025-07-01','M','reggeli, ebed, snack, vacsora',0);
INSERT INTO "meals" VALUES(161,3,'2025-07-02','M','reggeli, ebed, snack, vacsora',0);
INSERT INTO "meals" VALUES(162,3,'2025-07-03','M','reggeli, ebed, snack, vacsora',0);
INSERT INTO "meals" VALUES(163,3,'2025-07-06','M','reggeli, ebed, snack, vacsora',0);
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('customers',3);
INSERT INTO "sqlite_sequence" VALUES('meals',163);
COMMIT;
