# from sqlalchemy.orm import relationship
from celery import shared_task
from datetime import datetime as dt
from flask import (
    jsonify, session, json
)
from flask_login import (
    UserMixin, AnonymousUserMixin, current_user
)
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import TimedSerializer as Serializer

from werkzeug.security import (
    generate_password_hash, check_password_hash
)

from sqlalchemy import (
    BLOB, Boolean, Column, DateTime, Integer, String, 
    Text, ForeignKey, VARCHAR, VARBINARY, Float, join
)

# from sqlalchemy.ext.declarative.base import declared_attr
# from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm import relationship
from sqlalchemy.sql import and_, or_

from .compat import basestring
from .config import Config
# from .cache.cache_manager import flask_session_cache, connected_user_cache
from .extensions import db
from .utils import log


def reference_col(
    tablename, nullable = False, pk_name = "id",
    foreign_key_kwargs = None, column_kwargs = None
):
    """Column that adds a primary key to foreign key reference.

    Usage: ::
        category_id = reference_col('category')
        category = relationship('Category', backref='categories')

    You have to use both 'reference_col' and 'relationship' to
     create a complete bind.
    Both should be on the same table.
    """

    foreign_key_kwargs = foreign_key_kwargs or {}
    column_kwargs = column_kwargs or {}

    return Column(
        ForeignKey(f"{tablename}.{pk_name}", **foreign_key_kwargs),
        nullable=nullable, **column_kwargs
    )


class CRUDMixin(object):
    """
    Mixin that adds convenience methods for CRUD 
    (create, read, update, delete) operations.
    """
    @classmethod
    def roll_back(cls):
        return db.session.rollback()

    @classmethod
    def get(cls, id:int):
        """_summary_

        Args:
            id (int): _description_

        Returns:
            _type_: _description_
        """
        result = None
        if getattr(cls, 'id'):
            result = cls.query.get(id)
        log(__name__, result)
        return result


    @classmethod
    @shared_task(name='model_task.create_db_record')
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            self[attr] = value
        return self.save(commit=commit) or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    @classmethod
    def delete(cls, commit=True):
        """Remove the record from the database."""
        db.session.delete(cls)
        return commit and db.session.commit()
    
    
    # def filter(self, **kwargs):
    #     """_summary_
    #     """
    #     return self.query.filter(**kwargs)


    # def filter_by(self, **kwargs):
    #     return self.filter(and_(**kwargs))


class Model(CRUDMixin, db.Model):
    """
    Base model class that includes CRUD convenience methods.
    """

    __abstract__ = True
    created_at = Column(DateTime, default=dt.utcnow(), nullable=False)


# From Mike Bayer's "Building the app" talk
# https://speakerdeck.com/zzzeek/building-the-app
class SurrogatePK(object):
    """
    A mixin that adds a surrogate integer 'primary key' 
    column named ``id`` to any declarative-mapped class.
    """

    # __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, record_id):
        """
        [args]::
            record_id:int # -> Get record by ID.
        """
        if any(
            (
                isinstance(record_id, basestring) and record_id.isdigit(),
                isinstance(record_id, (int, float)),
            )
        ):
            return cls.query.get(int(record_id))
        return None


class DocumentsMixin(Model, SurrogatePK):
    """
    This defines the basic document recoding structure.
    """
    __abstract__=True
    url = Column(String(250), nullable=False, unique=True)


    def __repr__(self):
        """
        """
        return f'< Document:  - {self.url} >'


class RedisUserMixin:
    """
    """
    def __init__(self):
        """
        """
        permanent_session_id = session.get('_id')
        log(__name__, permanent_session_id)
        # self.user_data = json.loads(
        #     connected_user_cache.get_key(permanent_session_id)
        # )


    @classmethod
    def sio_connect(cls, sio_request_id:str):
        """
        """
        if current_user.is_authenticated:
            
            if cls.user_data:
                setattr(cls.user_data, 'sio_request_id', sio_request_id)
                setattr(cls.user_data, 'last_access', dt.now())
                # connected_user_cache.set_key(cls.permanent_session, json.dumps(cls.user_data))
                current_user._online()
                return cls.user_data
        return None


    @classmethod
    def sio_disconnect(cls):
        """
        """
        if current_user.is_authenticated:
            if cls.user_data:
                setattr(cls.user_data, 'sio_request_id', None)
                setattr(cls.user_data, 'last_access', dt.now())
                # connected_user_cache.set_key(cls.permanent_session, cls.user_data)
                current_user._offline()
                return True
        return None
    

    @classmethod
    def on_login(cls, browser:str, platform:str, flask_login_session_id:str):
        """
        """
        user_data = {
            "user_id": current_user.id,
            "connected": False,
            "sio_request_id": None,
            "platform": platform,
            "browser": browser,
            "session_id": flask_login_session_id,
            "is_anonymous": current_user.is_anonymous,
            "push_subscription": None,
            "last_access": dt.now(),
            "logged_out": False
        }
        # cached_user = connected_user_cache.set_key(cls.permanent_session, json.dumps(user_data))
        # return cached_user
    

    @classmethod
    def on_logout(cls):
        """
        """
        if cls.user_data:
            setattr(cls.user_data, "logged_out", True)
            setattr(cls.user_data, "last_access", dt.now())
            # connected_user_cache.set_key(cls.permanent_session, json.dumps(cls.user_data))
            # flask_session_cache.delete_key(cls.user_data.get('session_id'))
            return cls.user_data
        return None


class AnonymousUser(AnonymousUserMixin):
    is_anonymous = True
    is_active = False


class AuthMixin(UserMixin):
    __abstract__ = True
    """
    An abstract authentication mixin properties 
    class, for users who can login to the system.
    """
    phone = Column(String(14), unique=True, nullable=True)
    email = Column(String(80), unique=True, nullable=True)
    is_anonymous = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    confirmed = Column(Boolean, default=False)
    last_seen = Column(DateTime, default=dt.now())
    password_hash = Column(String(256), nullable=False)

    def get_id(self):
        """
        """
        return self.id
    
    @classmethod
    def get_by_id(cls, id:int):
        """
        """
        return cls.query.get(id)

    __mapper_args__ = {
        'polymorphic_identity': 'auth_mixin'
    }

    @property
    def password(self):
        """Protect password attribute from access."""
        raise AttributeError('Password is an abstracted attribute.')

    @password.setter
    def password(self, password):
        """Sets password"""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """Checks for password validity."""
        return check_password_hash(self.password_hash, password)

    def generate_token(self, expiration=3600, salt=None, **kwargs):
        """Generates token for email authentication."""
        serializer = Serializer(
            Config.SECRET_KEY,
            salt=bytes(
                salt or Config.SECRET_KEY,
                'latin-1'
            )
        )
        data = {
            'id': self.id
        }
        data.update(kwargs)
        return serializer.dumps(data)

    def confirm_token(self, token, salt=None):
        """Checks for validity of the passed token."""
        serializer = Serializer(
            Config.SECRET_KEY, 
            salt=salt or Config.SECRET_KEY
        )
        try:
            data = serializer.loads(token)
        except:
            return False, None
        if data.get('id') != self.id:
            return False, data
        return True, data

    def confirm_registration(self, token):
        """
        """
        result, _ = self.confirm_token(token)
        if not result:
            return False
        self.confirmed = True
        self.save()
        return True

    def confirm_new_email(self, token):
        """
        """
        result, data = self.confirm_token(token)
        if not result:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email = new_email).first() is not None:
            return False
        self.email = new_email
        self.save()
        return True

    def confirm_reset(self, token):
        """
        """
        result, data = self.confirm_token(token)
        new_password = data.get('new_password')
        if not result:
            return False
        self.password = new_password
        self.save()
        return True
    
    def _online(self):
        """
        """
        self.last_seen = dt.now()
        self.online = True
        self.save()
    
    def _offline(self):
        """
        """
        self.last_seen = dt.now()
        self.online = False
        self.save()

    def ping(self):
        """
        """
        self.last_seen = dt.utcnow()
        self.save()
