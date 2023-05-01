from flask import Flask

from .config import config_options
from .extensions import register_extensions

def register_blueprints(app):
    """
    """
    from .main import blueprint as main_bp
    app.register_blueprint(main_bp)

    from .auth import blueprint as auth_bp
    app.register_blueprint(auth_bp)


def create_app(config_name):
    """
    """
    app = Flask(__name__)
    app.config.from_object(config_options[config_name])

    register_extensions(app)
    register_blueprints(app)


    return app
    