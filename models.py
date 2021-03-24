from sqlalchemy import Column, Integer, String, Date, Enum, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
import os

database_path = "postgres://niflpdzmddyvym:d15bd058036354d888956bdb712df348f9905077991a725b1f3a81da259ac811@ec2-54-211-176-156.compute-1.amazonaws.com:5432/d2ups5itukv3f3"

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Movie
Have title and release year
'''
class Movie(db.Model):  
    __tablename__ = 'Movie'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

'''
Actor
Have name, age, and gender
'''
class Actor(db.Model):  
    __tablename__ = 'Actor'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }