from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()
Base=db.Model

dbse = db.session
