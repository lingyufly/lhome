--- 开启外键约束
PRAGMA FOREIGN_KEYS=ON;
-- Cash  Debit Card Credit Card Electronic Account
DROP TABLE IF EXISTS accounttype_tab;
CREATE TABLE accounttype_tab(
  accounttypeid INTEGER PRIMARY KEY AUTOINCREMENT,
  description VARCHAR(30),
  image VARCHAR(100) NOT NULL
);
INSERT INTO accounttype_tab VALUES(0,'Cash');
INSERT INTO accounttype_tab VALUES(1,'Debit Card');
INSERT INTO accounttype_tab VALUES(2,'Credit Card');
INSERT INTO accounttype_tab VALUES(3,'Electronic Account');

DROP TABLE IF EXISTS bank_tab;
CREATE TABLE bank_tab(
  bankid INTEGER PRIMARY KEY AUTOINCREMENT,
  accounttype INTEGER REFERENCES 'accounttype_tab'('id'),
  description VARCHAR(30) NOT NULL,
  image varchar(100) NOT NULL
);
INSERT INTO bank_tab VALUES();

DROP TABLE IF EXISTS account_tab;
CREATE TABLE account_tab(
  accountid INTEGER PRIMARY KEY AUTOINCREMENT,
  userid INTEGER REFERENCES 'user_tab'('id'),
  accountname VARCHAR(30) NOT NULL,
  image VARCHAR(100),
  amount REAL NOT NULL,
  createdate DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  description VARCHAR(100),
  accounttype INTEGER REFERENCES 'accounttype_tab'('id'),
  bank INTEGER REFERENCES 'bank_tab'('id'),
  limit REAL,
  used REAL,
  billingday DATE,
  repaymentday DATE
);

DROP TABLE IF EXISTS billbook_tab;
CREATE TABLE billbook_tab(
  bookid INTEGER PRIMARY KEY AUTOINCREMENT,
  bookname VARCHAR(30) NOT NULL,
  userid INTEGER REFERENCES 'user_tab'('id'),
  description VARCHAR(100),
  image VARCHAR(100),
  UNIQUE (bookname, userid)
);

DROP TABLE IF EXISTS billtype_tab;
CREATE TABLE billtype_tab(
  typeid INTEGER PRIMARY KEY AUTOINCREMENT,
  description VARCHAR(30)
  image VARCHAR(100)
);

DROP TABLE IF EXISTS category_tab;
CREATE TABLE category_tab(
  categotyid INTEGER PRIMARY KEY AUTOINCREMENT,
  description VARCHAR(30),
  tags varchar(200),
  image VARCHAR(100)
);

DROP TABLE IF EXISTS bill_tab;
CREATE TABLE bill_tab(
  billid INTEGER PRIMARY KEY AUTOINCREMENT,
  amount REAL NOT NULL,
  currency INTEGER,
  type INTEGER REFERENCES 'billtype_tab'('id'),
  account INTEGER REFERENCES 'account_tab'('id'),
  billbook INTEGER REFERENCES 'billbook_tab'('id'),
  createdate DATETIME DEFAULT CURRENT_TIMESTAMP,
  category INTEGER,
  tags VARCHAR(30),
  comments VARCHAR(100)
);


