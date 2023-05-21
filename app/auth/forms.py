# -*- coding: utf-8 -*-
"""Clients forms."""
from collections import namedtuple
from flask_babel import lazy_gettext
from flask_login import current_user
from flask_wtf import FlaskForm, Form
from wtforms import ValidationError
from wtforms.fields import (
    SubmitField, PasswordField, StringField, BooleanField
)
from flask_babel import lazy_gettext
from wtforms.validators import (
    DataRequired, Email, EqualTo, Length
)

from ..models import Users


class LoginForm(FlaskForm):
    email = StringField(
        lazy_gettext('Email'),
        validators=[DataRequired(),
        Length(1, 64),
        Email()],
        render_kw={
            'placeholder': lazy_gettext('Enter email')
        }
    )
    password = PasswordField(
        lazy_gettext('Password'),
        validators=[DataRequired()],
        render_kw={
            'placeholder': lazy_gettext('Enter password')
        }
    )
    remember = BooleanField(
        lazy_gettext('Keep me logged in')
    )


class ChangePasswordForm(FlaskForm):
    """
    """
    old_password = PasswordField(
        lazy_gettext('Old password'),
        validators=[DataRequired()]
    )
    new_password = PasswordField(
        lazy_gettext('New password'),
        validators=[
            DataRequired(),
            EqualTo(
                'new_password2',
                message=lazy_gettext('Passwords must match.')
            )
        ]
    )
    new_password2 = PasswordField(
        lazy_gettext('Confirm new password'),
        validators=[DataRequired()]
    )
    submit = SubmitField(
        lazy_gettext('Change password')
    )

    def validate_old_password(self, field):
        if not current_user.verify_password(field.data):
            raise ValidationError(
                lazy_gettext('Invalid old password.')
            )

    def validate_new_password(self, field):
        if self.old_password.data == field.data:
            raise ValidationError(
                lazy_gettext('New password is the same as old password.')
            )


class ChangeEmailForm(FlaskForm):
    new_email = StringField(
        lazy_gettext('New email'),
        validators=[
            DataRequired(), Length(1, 64), Email()
        ]
    )
    password = PasswordField(
        lazy_gettext('Password'),
        validators=[DataRequired()]
    )
    submit = SubmitField(
        lazy_gettext('Change email')
    )


    def validate_new_email(self, field):
        if current_user.email == field.data.lower():
            raise ValidationError(
                lazy_gettext('This is your current email.')
            )
        if Users.query.filter_by(email=field.data.lower()).first():
            raise ValidationError(
                lazy_gettext('Email already registered.')
            )


    def validate_password(self, field):
        if not current_user.verify_password(field.data):
            raise ValidationError(
                lazy_gettext('Invalid password.')
            )


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(
        lazy_gettext('Email'),
        validators=[
            DataRequired(), Length(1, 64), Email()
        ]
    )
    submit = SubmitField(
        lazy_gettext('Reset password')
    )


    def validate_email(self, field):
        if Users.query.filter_by(email=field.data.lower()).first() is None:
            raise ValidationError(
                lazy_gettext('Unknown email address.')
            )


class ResetPasswordForm(FlaskForm):
    email = StringField(
        lazy_gettext('Email'),
        validators=[
            DataRequired(), Length(1, 64), Email()
        ]
    )
    password = PasswordField(
        lazy_gettext('New password'),
        validators=[
            DataRequired(), EqualTo(
                'password2',
                message=lazy_gettext('Passwords must match.')
            )
        ]
    )
    password2 = PasswordField(
        lazy_gettext('Confirm password'),
        validators=[DataRequired()]
    )
    submit = SubmitField(
        lazy_gettext('Reset password')
    )

 
    def validate_email(self, field):
        if Users.query.filter_by(email=field.data.lower()).first() is None:
            raise ValidationError(
                lazy_gettext('Unknown email address.')
            )
