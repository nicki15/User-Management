from flask import Blueprint, jsonify, request
import json

from database.database import db, User


user_blueprint = Blueprint('user_blueprint', __name__)


@user_blueprint.route("/")
def index():
    return 'hallo'


@user_blueprint.route("/add-user",methods=['POST'])
def add_user():
    data = json.loads(request.get_data().decode("utf-8"))
    try:
        user = User(name=data['name'], email=data['email'])
        user.set_password(data['pw'])
        user.save_to_db()
        message = "User successfully added"
    except Exception as ex:
        message = "User already exists"
    finally:
        return_code = 404 if 'already exists' in message else 200
        return jsonify({
            "status": message
        }), return_code


@user_blueprint.route("/get-user", methods=['POST'])
def get_user():
    data = json.loads(request.get_data().decode("utf-8"))
    payload = None
    status_code = 404
    message = ""
    try:
        u = User.query.filter_by(email=data['email']).first()
        provided_password = data['pw']
        if u.check_password(provided_password):
            message = "Successfully retrieved user"
            payload = u.__repr__()
            status_code = 200
        else:
            message = "wrong password"
    except Exception as ex:
        print("[!] ", ex)
        message = "Unexpected error occurred"
    finally:
        return jsonify({
            'status': message,
            'payload': payload
        }), status_code
