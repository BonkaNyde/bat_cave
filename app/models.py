# -*- coding: utf-8 -*-
"""all the models"""
from datetime import datetime
from email.policy import default
from enum import unique
from flask import (
    jsonify, g
)
from sqlalchemy import (
    BLOB, Boolean, Column, DateTime,
    Integer, String, Text, ForeignKey, 
    VARCHAR, VARBINARY, Float, join, JSON
)
from sqlalchemy.orm import (
    relationship, backref
)
from .mixins import (
    AnonymousUser,
    AuthMixin,
    Model, SurrogatePK, 
    reference_col, DocumentsMixin
)
from .extensions import login_manager


class Logs(Model):
    """
    """
    id = Column(Integer, primary_key=True)
    user_id = reference_col('users')
    action = Column(String, nullable=False)
    action_url = Column(String, nullable=False)
    users = relationship('Users', backref=backref('logs', lazy='dynamic'))



class Users(AuthMixin, Model):
    """
    any account that has login capabilities is under this class
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    type = Column(String(150), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'users',
        'polymorphic_on': type
    }

    @classmethod
    def get_push_subscriptions(cls, user_id:int):
        user = cls.query.get(user_id)
        return [session_data for session_data in user.login_history.all() if session_data.push_subscription]



class LoginHistory(Model):
    """
    """
    __tablename__ = 'login_history'
    id = Column(Integer, primary_key=True)
    user_id = reference_col('users')
    session_id = Column(String, nullable=False)
    session_sid = Column(String, nullable=False)
    browser = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    push_subscription = Column(JSON)
    remember_cookie = Column(Boolean, default=False)
    user = relationship('Users', backref=backref('login_history', lazy='dynamic'))

    __mapper_args__ = {
        'polymorphic_identity': 'login_history'
    }

    @classmethod
    def get_session(cls, session_id:str):
        """_summary_

        Args:
            session_id (str): _description_

        Returns:
            _type_: _description_
        """
        return cls.query.filter_by(session_id=session_id).first()


class Notification(Model):
    """
    """
    __tablename__ = 'notification'
    id = Column(Integer, primary_key=True)
    for_user_id = reference_col('users')
    body = Column(String(250), nullable=False)
    read = Column(Boolean)
    for_user = relationship('Users', backref=backref('notifications', lazy='dynamic'))


class Message(Model):
    """
    """
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    from_user_id = reference_col('users')
    to_user_id = reference_col('users')
    body = Column(Text, nullable=False)
    from_user = relationship('Users', foreign_keys=[from_user_id], backref=backref('messages_sent', lazy='dynamic'))
    to_user = relationship('Users', foreign_keys=[to_user_id], backref=backref('messages', lazy='dynamic'))


class MessageMedia(Model):
    __tablename__ = 'message_media'
    id = Column(Integer, primary_key=True)
    message_id = reference_col('message')
    media_path = Column(String, nullable=False)
    message = relationship('Message', backref=backref('media', lazy='dynamic'))


class Document(DocumentsMixin):
    """
    """
    __tablename__ = 'document'

