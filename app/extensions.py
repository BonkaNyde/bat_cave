# -*- coding: utf-8 -*-
from celery import Celery
from flask import (
    globals,
    request
)
from flask_babel import (
    Babel,
    lazy_gettext
)
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import (
    AnonymousUserMixin,
    LoginManager
)
from flask_migrate import Migrate
from flask_mail import (
    email_dispatched,
    Mail
)
from flask_redis import FlaskRedis
# from flask_rq2 import RQ
from flask_session import Session
from flask_socketio import SocketIO
# from flask_simplemde import SimpleMDE
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from mockredis import MockRedis

# from .utils import log
# from .config import Config


babel = Babel()
bcrypt = Bcrypt()
# celery = Celery()

cors = CORS()
csrf_protect = CSRFProtect()
db = SQLAlchemy()
debug_toolbar = DebugToolbarExtension()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.localize_callback = lazy_gettext
login_manager.anonymous_user = AnonymousUserMixin
login_manager.refresh_view = 'auth.login'
mail = Mail()
migrate = Migrate()
redis_client = FlaskRedis()
# simple = SimpleMDE()
session = Session()
socket_io = SocketIO()


class MockRedisWrapper(MockRedis):
    '''A wrapper to add the `from_url` classmethod'''

    @classmethod
    def from_url(cls, *args, **kwargs):
        return cls(*args, **kwargs)


def make_celery(app):
    celery = Celery(app.import_name)
    celery.conf.update(app.config.get('CELERY_CONFIG'))
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


def register_extensions(app):
    """Initialize app extensions."""
    babel.init_app(app)
    bcrypt.init_app(app)
    celery = make_celery(app)
    celery.set_default()
    celery.autodiscover_tasks()
    cors.init_app(app, allow_headers='*', origins=['http://0.0.0.0:5001', 'http://0.0.0.0:5002', 'http://0.0.0.0:5003', 'http://0.0.0.0:5004'], supports_credentials=True)
    csrf_protect.init_app(app)
    db.init_app(app)
    debug_toolbar.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    mail.init_mail(app.config, app.debug)
    migrate.init_app(app, db)
    if app.debug:
        redis_client.from_custom_provider(MockRedisWrapper)
    else:
        redis_client.init_app(app)
    # redis_queue.init_app(app)
    session.init_app(app)
    # simple.init_app(app)
    
    socket_io.init_app(
        app, 
        async_mode='gevent', 
        message_queue=app.config.get('REDIS_URL'),
        channel='school_system',
        engineio_logger=True,
        cors_allowed_origins = '*', 
        manage_session=True,
        logger=app.debug
    )
    app.app_context().push()
    return celery
    # def log_message(message, app, level='info'):
    #     if app.debug:
    #         getattr(app.logger, level)(f'[** { message.subject } **] {message}')
    #     # app.logger.debug(message.subject)

    # email_dispatched.connect(log_message)
    
