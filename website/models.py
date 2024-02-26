from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func



class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    breed = db.Column(db.String(100))
    sex = db.Column(db.String(10))
    age = db.Column(db.String(20))
    spayed_neutered = db.Column(db.String(10))
    personality_description = db.Column(db.String(1000))
    other_info = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    pets = db.relationship('Pet')