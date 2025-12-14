from flask import Flask
from app.extensions import ma
from app.models import db
from app.blueprint.customers import customers_bp
from app.blueprint.service_tickets import tickets_bp
from app.blueprint.mechanic import mechanics_bp


def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')

    #initialize extensions
    db.init_app(app)
    ma.init_app(app)

    #register blueprints

    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(tickets_bp, url_prefix='/service-tickets')
    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')


    return app