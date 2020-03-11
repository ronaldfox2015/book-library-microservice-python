# project/server/models.py

import datetime

from flask import current_app

from project.server import db, bcrypt


# from project.server.db import Column


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Importante
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    test = db.Column(db.Boolean)

    def __init__(self, email, password, admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get("BCRYPT_LOG_ROUNDS")
        ).decode("utf-8")
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return "<User {0}>".format(self.email)


class Parrent(db.Model):
    __tablename__ = "parrent"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250))


class Students(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250))
    last_name = db.Column(db.String(250))
    age = db.Column(db.Integer)
    email = db.Column(db.String(250))

    def __init__(self, *args, **kwargs):
        self.name = kwargs['name']
        self.last_name = kwargs['last_name']
        self.age = kwargs['age']
        self.email = kwargs['email']

    @property
    def serializer(self):
        return {
            'name': self.name,
            'last_name': self.last_name,
            'age': self.age,
            'email': self.email
        }

    def __str__(self):
        return f'{self.name} {self.last_name}'


class Clients(db.Model):
    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250))
    rs = db.relationship('Restaurants')

    @property
    def serializer(self):
        return {
            'name': self.name,
        }

    def __str__(self):  ## __repr__
        return f'{self.name}'


class Menus(db.Model):
    __tablename__ = "menus"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250))
    price = db.Column(db.Float)
    rs = db.relationship('Restaurants')

    def __init__(self, *args, **kwargs):
        self.name = kwargs['name']
        self.price = kwargs['price']

    @property
    def serializer(self):
        return {
            'name': self.name,
        }

    def __str__(self):
        return f'{self.name}'


class Restaurants(db.Model):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250))
    clients = db.Column(db.Integer, db.ForeignKey('clients.id'))
    menus = db.Column(db.Integer, db.ForeignKey('menus.id'))

    def __init__(self, *args, **kwargs):
        self.name = kwargs['name']
        self.clients = kwargs['client']
        self.menus = kwargs['menu']

    @property
    def serializer(self):
        return {
            'name': self.name,
        }

    def __str__(self):
        return f'{self.name} {self.menus.name}'

