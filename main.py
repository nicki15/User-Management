from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

from database.database import db

from helpers import configuration
from resources.UserRegistration import UserRegistration


jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = configuration.SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + configuration.DB_NAME
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['JWT_SECRET_KEY'] = configuration.JWT_SECRET_KEY
    app.config['JWT_BLACKLIST_ENABLED'] = configuration.JWT_BLACKLIST_ENABLED
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = configuration.JWT_BLACKLIST_TOKEN_CHECKS
    register_extensions(_app=app)
    return app


def register_extensions(_app: Flask):
    db.init_app(_app)
    jwt.init_app(_app)


def setup_api_endpoints(_app: Flask):
    api = Api(_app)
    api.add_resource(UserRegistration, '/registration')


def setup_database(_app: Flask):
    with _app.app_context():
        db.create_all()


if __name__ == "__main__":
    flask_app = create_app()
    setup_database(_app=flask_app)
    setup_api_endpoints(_app=flask_app)
    flask_app.run(port=8080, debug=True)
