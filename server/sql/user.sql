--- 开启外键约束
PRAGMA FOREIGN_KEYS=ON;

DROP TABLE IF EXISTS user_tab;
CREATE TABLE user_tab(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(30) NOT NULL UNIQUE,
  password VARCHAR(127) NOT NULL,
  createdate DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  description VARCHAR(100),
  gender VARCHAR(6),
  birthday DATETIME NOT NULL DEFAULT CURRENT_DATE,
  email VARCHAR(127),
  mobile VARCHAR(11),
  photo VARCHAR(100),
  isadmin BOOL NOT NULL DEFAULT 0
);
INSERT INTO user_tab(name, password, description, isadmin) values('admin', 'admin', 'administrator', 1);