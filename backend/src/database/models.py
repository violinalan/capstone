import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

# database_name = "capstone"
# database_path = "postgresql://{}/{}".format('alan:vocisuj3@localhost:5432', database_name)
database_path = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)
# SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

class Movie(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(100), unique=True)
    year_released = Column(Integer)

    def long(self):
        return {
            'id': self.id,
            'title': self.title,
            'year_released': self.year_released
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.long())

class Actor(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    age = Column(Integer)
    gender = Column(String(10))

    def long(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.long())