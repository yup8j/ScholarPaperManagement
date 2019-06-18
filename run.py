from flask import Flask, g
from backend.app import api_bp
from backend.models import register_database
from mongoengine import connect


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
    connect(
        db='test_11',
        host='mongodb://dds-wz9f23f0cffe4b341504-pub.mongodb.rds.aliyuncs.com:3717,dds-wz9f23f0cffe4b342338-pub.mongodb.rds.aliyuncs.com:3717',
        username='root',
        password='qwerty2019()-=',
        authentication_source='admin',
        authentication_mechanism='SCRAM-SHA-1',
        replicaset='mgset-15064123'
    )


def register_routes(app):
    app.register_blueprint(api_bp)


application = create_app(debug=True)
if __name__ == '__main__':
    application.run()
