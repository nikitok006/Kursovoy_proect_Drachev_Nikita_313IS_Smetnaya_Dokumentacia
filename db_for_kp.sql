BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Estimate_Resources" (
	"id"	INTEGER,
	"estimate_id"	INTEGER NOT NULL,
	"resource_id"	INTEGER NOT NULL,
	"quantity"	REAL NOT NULL,
	"total_cost"	REAL NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("estimate_id") REFERENCES "Estimates"("id") ON DELETE CASCADE,
	FOREIGN KEY("resource_id") REFERENCES "Resources"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "Estimates" (
	"id"	INTEGER,
	"project_id"	INTEGER NOT NULL,
	"total_cost"	REAL NOT NULL,
	"created_at"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("project_id") REFERENCES "Projects"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "Projects" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL,
	"customer"	TEXT NOT NULL,
	"budget"	REAL NOT NULL,
	"status"	TEXT NOT NULL,
	"id_estimator"	INT NOT NULL,
	"id_project_manager"	INT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("id_estimator") REFERENCES "Users"("login") ON DELETE CASCADE,
	FOREIGN KEY("id_project_manager") REFERENCES "Users"("login") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "Resources" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL,
	"unit"	TEXT NOT NULL,
	"cost_per_unit"	REAL NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Users" (
	"login"	TEXT,
	"name"	TEXT NOT NULL,
	"role"	TEXT NOT NULL CHECK("role" IN ('сметчик', 'проектный менеджер')),
	"email"	TEXT NOT NULL,
	"password"	TEXT NOT NULL,
	PRIMARY KEY("login")
);
INSERT INTO "Projects" ("id","name","customer","budget","status","id_estimator","id_project_manager") VALUES (1,'Строительство жилого комплекса','ООО Жилстрой',50000000.0,'В процессе','user1','user2'),
 (2,'Ремонт офисного здания','АО ОфисСервис',20000000.0,'Запланирован','user1','user2'),
 (3,'Реконструкция школы','Управление образования',30000000.0,'В процессе','user3','user4'),
 (4,'Строительство торгового центра','ООО ТЦ',70000000.0,'Завершен','user5','user4'),
 (5,'Строительство больницы','Минздрав',100000000.0,'В процессе','user3','user4');
INSERT INTO "Resources" ("id","name","unit","cost_per_unit") VALUES (1,'Бетон','м³',4000.0),
 (2,'Арматура','кг',50.0),
 (3,'Кирпич','шт',20.0),
 (4,'Песок','м³',600.0),
 (5,'Цемент','кг',10.0);
INSERT INTO "Users" ("login","name","role","email","password") VALUES ('user1','Иван Иванов','сметчик','ivanov@example.com','password1'),
 ('user2','Мария Петрова','проектный менеджер','petrova@example.com','password2'),
 ('user3','Алексей Смирнов','сметчик','smirnov@example.com','password3'),
 ('user4','Ольга Сидорова','проектный менеджер','sidorova@example.com','password4'),
 ('user5','Дмитрий Кузнецов','сметчик','kuznetsov@example.com','password5');
COMMIT;
