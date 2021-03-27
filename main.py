from flask import Flask
from database.database import db

from helpers import configuration
from routes.routes import user_blueprint


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = configuration.SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + configuration.DB_NAME
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    register_extensions(_app=app)
    register_blueprints(_app=app)
    return app


def register_extensions(_app: Flask):
    db.init_app(_app)


def register_blueprints(_app: Flask):
    _app.register_blueprint(user_blueprint, url_prefix='/')


def setup_datebase(_app: Flask):
    with _app.app_context():
        db.create_all()


if __name__ == "__main__":
    flask_app = create_app()
    setup_datebase(_app=flask_app)
    flask_app.run(port=8080, debug=True)
