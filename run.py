from flask import Flask, g
from backend.app import api_bp


def create_app():
    app = Flask(__name__)
    app.debug = True
    return app


def register_routes(app):
    app.register_blueprint(api_bp, url_prefix='/api')


if __name__ == '__main__':
    create_app().run()
