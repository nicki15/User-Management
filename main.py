import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from helpers import configuration
from DBManager.DBManager import create_database, add_newuser, get_user_by_id, get_user_by_email



app = Flask(__name__)

app.config["SECRET_KEY"] = configuration.SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + configuration.DB_NAME

db = SQLAlchemy(app=app)

class User(db.Model):
    id = db.Column('user_id', db.Integer, primary_key = True)
    name = db.Column(db.String(), unique = True)
    email = db.Column(db.String(), unique = True)
    password = db.Column(db.String())

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


@app.route("/")
def index():
    return 'hallo'

@app.route("/add-user",methods=['POST'])
def add_user():
    data = json.loads(request.get_data().decode("utf-8"))
   # name = data['name']
   # email = data['email']
    #pw = data['pw']
    #query_result = add_newuser(name, email, pw)
    try:
        user = User(name=data['name'], email=data['email'])
        user.set_password(data['pw'])
        db.session.add(user)
        db.session.commit()
        message = "User successfully added"
    except Exception as ex:
        print(ex)
        message = "User already exists"
    finally:
        return_code = 404 if 'already exists' in message else 200
        return jsonify({
            "status": message
        }), return_code

if __name__ == "__main__":
    db.create_all()
    app.run(port=8080, debug = True)
