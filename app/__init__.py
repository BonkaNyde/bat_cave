# -*- coding: utf-8 -*-
# """Application initialization"""
from flask import (
    Flask, render_template
)
import logging, sys
from werkzeug.middleware.proxy_fix import ProxyFix
# # from queue import Queue
# from rq import Queue
from gevent.queue import Queue
import os

from .config import config_options
from .extensions import (
    register_extensions
)
from .utils import log


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)


def register_blueprints(app):
    """Register Flask blueprints."""

    from .auth import blueprint as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .sys_admin import blueprint as sys_admin_blueprint
    app.register_blueprint(sys_admin_blueprint, url_prefix='/sys_admin')

    from .main import blueprint as main_blueprint
    app.register_blueprint(main_blueprint)


def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        # log(__name__, f"{app.static_url_path}/errors/{error_code}.html")
        return render_template(f'errors/{error_code}.html', title=error_code), error_code
        
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def create_app(environment):
    """
    Create application factory, as explained here: 
    http://flask.pocoo.org/docs/patterns/appfactories/.

        :param config_object: The configuration object to use.
    """
    # Create app instance.
    app = Flask(__name__)
    app.config.from_object(
        config_options.get(environment)
    )
    celery = register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    configure_logger(app)

    from flask_sslify import SSLify
    if 'DYNO' in os.environ:  # only trigger SSLify if the app is running on Heroku
        SSLify(app)
        
    app.queue = Queue()
    app.wsgi_app = ProxyFix(app.wsgi_app)

    return app, celery
