from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


db = SQLAlchemy()


class User(db.Model):
    id = db.Column('user_id', db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    email = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    register_date = db.Column(db.DateTime())

    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.register_date = datetime.now()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def set_password(self, password):
        self.password = generate_password_hash(password=password, salt_length=32)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"User: [name: {self.name}, email={self.email}, user_id={self.id}]"
