# -*- coding: utf-8 -*-
"""Application configuration.

Most configuration is set via environment variables.

For local development, use a .env file to set
environment variables.
"""
import hashlib, os, redis
from environs import Env
from pytz import timezone
from os.path import (
    join, dirname, abspath
)
from webnoti import get_private_key
from webnoti.utils import encode_public_key, ec
from webnoti.encryption import encrypt_data, create_info

# from .celery_tasks.crons import beats


env = Env()
env.read_env()

class Config:
    """
    General application configuration
    """
    BASE_DIR = abspath(dirname(__file__))
    
    # # # Basic general settings # # # 
    CACHE_TYPE = env.str('CACHE_TYPE')
    CACHE_DEFAULT_TIMEOUT = env.str('CACHE_DEFAULT_TIMEOUT')

    # # # Security configuration # # # 
    SECRET_KEY = hashlib.sha256(bytes(env.str('SECRET_KEY'), 'latin-1')).hexdigest()
    SESSION_PROTECTION = env.str('SESSION_PROTECTION')
    BCRYPT_LOG_ROUNDS = env.int("BCRYPT_LOG_ROUNDS")

    # # # Google OAUTH 
    CLIENT_ID = env.str('GOOGLE_CLIENT_ID')
    CLIENT_SECRET = env.str('CLIENT_SECRET')
    CLIENT_SECRETS_JSON = env.json('CLIENT_SECRETS_JSON')
    GOOGLE_CLIENT_SCOPES = env.list('GOOGLE_CLIENT_SCOPES')
    GOOGLE_CB_REDIRECT_URI = env.str('GOOGLE_CB_REDIRECT_URIS')
    OAUTHLIB_INSECURE_TRANSPORT = env.bool('OAUTHLIB_INSECURE_TRANSPORT')

    # # # General Mail Configuration # # # 
    MAIL_SERVER = env.str('MAIL_SERVER')
    MAIL_PORT = env.int('MAIL_PORT')
    MAIL_USERNAME = env.str('MAIL_USERNAME')
    MAIL_PASSWORD = env.str('MAIL_PASSWORD')
    MAIL_USE_TLS = env.bool('MAIL_USE_TLS')
    MAIL_USE_SSL = env.bool('MAIL_USE_SSL')
    MAIL_ASCII_ATTACHMENTS = None
    APP_ADMIN = env.str('ADMIN_MAIL_USERNAME')
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

    # # # Babel Configuration # # # 
    BABEL_DEFAULT_LOCALE = 'en' #env.str('BABEL_DEFAULT_LOCALE')
    BABEL_DEFAULT_TIMEZONE = env.str('BABEL_DEFAULT_TIMEZONE')
    BABEL_DOMAIN = env.str('BABEL_DOMAIN')
    BABEL_TRANSLATION_DIRECTORIES = env.str('BABEL_TRANSLATION_DIRECTORIES')
    SUPPORTED_LANGUAGES = {
        'en': 'English',
        'ru': 'Russian',
        'es': 'Spanish'
    }

    # # # Uploads Configuration # # # 
    SEND_FILE_MAX_AGE_DEFAULT = env.int("SEND_FILE_MAX_AGE_DEFAULT")
    MAX_CONTENT_LENGTH = env.int('MAX_CONTENT_LENGTH')
    UPLOAD_FOLDER = env.str('UPLOADED_PHOTOS_DEST')
    UPLOAD_DIR = os.sep.join([BASE_DIR, UPLOAD_FOLDER])
    ALLOWED_EXTENSIONS = {
        'txt', 'pdf', 
        'png', 'jpg', 
        'jpeg', 'gif'
    }

    # # # Redis Configuration # # # 
    """
        If your redis service is configured with a password, set 
        REDIS_WITH_PASSWORD=1 in the '.env' file. You should 
        then provide your REDIS_PASSWORD=<your_redis_password>.        
    """ 
    REDIS_HOST = env.str('REDIS_HOST')
    REDIS_PORT = env.int('REDIS_PORT')
    REDIS_PASSWORD = env.str('REDIS_PASSWORD')
    REDIS_URL = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}'
    # REDIS_CACHE_URL = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0'
    # REDIS_METRICS_URL = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/2'

    # RQ_DEFAULT_DB = 1
    # RQ_REDIS_URL = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{RQ_DEFAULT_DB}'
    # RQ_LOW_URL = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/2'
    # RQ_QUEUES = ['default']
    # RQ_ASYNC = True

    # # # Flask Session configuration # # #
    SESSION_TYPE = env.str('SESSION_TYPE')
    SESSION_COOKIE_SECURE = True
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = '_sid_-'
    SESSION_REDIS = redis.from_url(f'{REDIS_URL}/4')

    # # # celery configuration # # # 
    DEFAULT_LOCALE = 'Africa/Nairobi'
    LOCALE_TIMEZONE = timezone(DEFAULT_LOCALE)
    CELERY_CONFIG = {
        'accept_content': ['application/json'],
        'broker_url': REDIS_URL,
        'result_backend': REDIS_URL,
        'result_serializer': 'json',
        'task_serializer': 'json',
        'include': ['app.celery_tasks.tasks'],
        'enable_utc': True,
        'timezone': DEFAULT_LOCALE,
        # 'beat_schedule': beats
    }
    # CELERY_BROKER_URL = REDIS_URL
    # CELERY_RESULT_BACKEND = REDIS_URL

    # WEBNOTI CONF
    PERM_FILE_NAME = env.str('PERM_FILE_NAME', 'priv_key')
    PERM_FILE_EXT = env.str('PERM_FILE_EXT', 'pem')
    WEBNOTI_PASS = b'kwangwaru'
    # from base64 import urlsafe_b64encode
    # WEBNOTI_PERM_FILE = f'{BASE_DIR}{os.sep}{PERM_FILE_NAME}.{PERM_FILE_EXT}'
    # WEBNOTI_PRIVATE_KEY = get_private_key(WEBNOTI_PERM_FILE, WEBNOTI_PASS, generate=bool)
    # ec.EllipticCurvePublicKey().from_encoded_point(WEBNOTI_PRIVATE_KEY.curve, WEBNOTI_PERM_FILE.encode('latin-1'), WEBNOTI_PRIVATE_KEY.public_key())
    # WEBNOTI_SERVER_KEY = encode_public_key(WEBNOTI_PRIVATE_KEY.public_key())
    

    # database configuration
    DB = env.str('DB')
    DB_DRIVER = env.str('DB_DRIVER')
    DB_USER = env.str('DB_USERNAME')
    DB_PASS = env.str('DB_PASSWORD')
    DB_NAME = env.str('DB_NAME')
    SQLALCHEMY_DATABASE_URI = f"{DB}+{DB_DRIVER}://{DB_USER}:{DB_PASS}@localhost/{DB_NAME}"


class DevConfig(Config):
    """
    """
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG_TB_ENABLED = True

    MAIL_DEBUG = True
    # MAIL_SUPPRESS_SEND = True

    # SERVER_NAME = '0.0.0.0:5000'


class ProdConfig(Config):
    """
    """
    DEBUG = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG_TB_ENABLED = False


class TestConfig(Config):
    """
    """
    TESTING = True
    DEBUG_TB_ENABLED = True

    def init_app(self, app):
        app.config.update(self)


config_options = {
    'development': DevConfig,
    'production': ProdConfig,
    'testing': TestConfig
}
