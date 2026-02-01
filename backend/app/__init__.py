# app/__init__.py

from flask import Flask, app
from app.config import Config
from app.extensions import db, migrate, jwt, mail, cors
from flask.cli import with_appcontext
import click
from app.seed import seed_roles_and_plans
from app.routes.auth import auth_bp
from app.routes.test import test_bp
from app.routes.api_keys import api_keys_bp
from app.routes.upload import upload_bp



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)
    cors.init_app(app, supports_credentials=True)

    from app.models import (
        company,
        role,
        user,
        api_key,
        upload,
        customer,
        prediction,
        risk_timeline,
        churn_driver,
        alert_rule,
        alert_event,
        recommendation,
        plan,
        usage_log,
    )

    @app.cli.command("seed")
    @with_appcontext
    def seed():
        seed_roles_and_plans()


    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(test_bp, url_prefix="/api/test")
    app.register_blueprint(api_keys_bp, url_prefix="/api/api-keys")
    app.register_blueprint(upload_bp, url_prefix="/api/upload")

    return app

