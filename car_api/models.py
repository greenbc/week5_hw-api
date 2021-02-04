from car_api import app, db, login_manager
import uuid
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

import secrets

from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default='')
    last_name = db.Column(db.String(150), nullable = True, default='')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default='')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default='')
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    drone = db.relationship('Car', backref = 'owner', lazy = True)

    def __init__(self, email, first_name='', last_name='',id = '',password='', token = '', g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been added to the database'

class Car(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    make = db.Column(db.String(150))
    model = db.Column(db.String(150))
    color = db.Column(db.String(150))
    price = db.Column(db.Integer)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable = False)

    def __init__(self,make,model,color,price,user_id):
        self.make = make
        self.model = model
        self.color = color
        self.price = price
        self.user_id = user_id

    def __repr__(self):
        return f'The following Car has been added: {self.make} {self.model} which belongs to {self.user_id}'

    def to_dict(self):
        return {
            "id": self.id,
            "make": self.make,
            "model": self.model,
            "color": self.color,
            "price": self.price
        }