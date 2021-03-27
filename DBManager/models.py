from main import db

class User(db.Model):
    id = db.Column('user_id', db.Integer, primary_key = True)
    name = db.Column(db.String(), unique = True)
    email = db.Column(db.String(), unique = True)
    passwort = db.Column(db.String())

    def __init__(self, name, email, passwort):
        self.name = name
        self.email = email
        self.passwort = passwort

