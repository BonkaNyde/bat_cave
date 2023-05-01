from flask import Flask
from celery import Celery, Task
from flask_login import LoginManager
from flask_babel import Babel, lazy_gettext
from flask_redis import FlaskRedis


babel = Babel()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.localize_callback = lazy_gettext()
# login_manager.user_loader = load_user
redis = FlaskRedis()


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


def register_extensions(app):
    babel.init_app(app)
    celery_init_app(app)
    login_manager.init_app(app)
    redis.init_app(app)

