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

    @classmethod
    def find_by_username(cls, username: str):
        return cls.query.filter_by(name=username).first()

    def set_password(self, password):
        self.password = generate_password_hash(password=password, salt_length=32)

    @staticmethod
    def check_password(password, _hash):
        return check_password_hash(pwhash=_hash, password=password)

    def __repr__(self):
        return f"User: [name: {self.name}, email={self.email}, user_id={self.id}]"


class RevokedToken(db.Model):

    token_id = db.Column(db.Integer, primary_key=True)
    revoked_token = db.Column(db.String())
    revocation_date = db.Column(db.DateTime())
    issuer_id = db.Column(db.Integer, unique=False)

    def __init__(self, _token, _issuer_id):
        self.revoked_token = _token
        self.issuer_id = _issuer_id
        self.revocation_date = datetime.now()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, _jti):
        query = cls.query.filter_by(revoked_token=_jti).first()
        return bool(query)
