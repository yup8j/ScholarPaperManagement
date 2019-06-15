from flask import Flask, g
from backend.app import api_bp
from backend.models import register_database


def create_app(**config):
    app = Flask(__name__)
    register_config(app, config)
    register_database(app)
    register_routes(app)
    return app


def register_config(app, config):
    if config.get('debug') is True:
        app.debug = True

    from backend.config import default
    app.config.from_object(default)


def register_routes(app):
    app.register_blueprint(api_bp)


if __name__ == '__main__':
    create_app(debug=True).run()