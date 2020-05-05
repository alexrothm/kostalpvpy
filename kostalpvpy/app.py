from flask import Flask, render_template
from config import Config

from kostalpvpy.extensions import cache, db, migrate
from kostalpvpy import home


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    return app


def register_extensions(app):
    # assets.init_app(app)
    cache.init_app(app, config={"CACHE_TYPE": "simple"})
    db.init_app(app)
    migrate.init_app(app, db)

    return None


def register_blueprints(app):
    app.register_blueprint(home.controller.bp_home)

    return None


def register_errorhandlers(app):
    def render_error(error):
        error_code = getattr(error, "code", 500)
        return render_template("{0}.html".format(error_code)), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None
