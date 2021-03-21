import json
from flask import Flask, request, jsonify

from DBManager.DBManager import create_database, add_newuser, get_user_by_id, get_user_by_email


if __name__ == "__main__":

    app = Flask(__name__)

    @app.route("/")
    def index():
        return 'hallo'

    @app.route("/add-user",methods=['POST'])
    def add_user():
        data = json.loads(request.get_data().decode("utf-8"))
        name = data['name']
        email = data['email']
        pw = data['pw']
        query_result = add_newuser(name, email, pw)

        return jsonify({
            "status": query_result[1]
        })

    app.run(port=8080, debug = True)
