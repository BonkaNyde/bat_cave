# # -*- coding: utf-8 -*-
from datetime import datetime
from flask import current_app
from flask_babel import lazy_gettext
from flask_login import current_user
from flask_wtf import (
    FlaskForm, Form
)
from sqlalchemy.sql.expression import and_
from wtforms import ValidationError
from wtforms.fields import (
    SelectField, SubmitField,
    SelectMultipleField, PasswordField,
    StringField, FloatField, BooleanField, 
    FieldList, HiddenField, FileField,
    Field, Flags, FormField, IntegerField,
    EmailField, SearchField, DateField,
    DateTimeField, DateTimeLocalField,
    DecimalField,IntegerRangeField, TelField,
    TimeField, URLField, choices
)
from wtforms.validators import (
    DataRequired, NumberRange, EqualTo,
    IPAddress, MacAddress, Length, Optional,
    InputRequired, Regexp, URL, AnyOf, NoneOf
)
from wtforms_alchemy import model_form_factory
from sqlalchemy import (
    and_, any_, func
)
from sqlalchemy.orm import (
    aliased, join, outerjoin, session
)
from ..models import (
    Document, Users
)


def compute_base_form(form_type=FlaskForm):
    return model_form_factory(form_type)

ModelFlaskForm = compute_base_form()
ModelForm = compute_base_form(form_type=Form)

class PersonData(ModelFlaskForm):
    first_name = StringField(
        lazy_gettext('First Name'),
        validators=[DataRequired()],
        render_kw={
            "placeholder": "John...",
            "data-position": "bottom right"
        }
    )
    last_name = StringField(
        lazy_gettext('Last Name'),
        validators=[DataRequired()],
        render_kw={
            "placeholder": "Doe...",
            "data-position": "bottom right"
        }
    )
    sur_name = StringField(
        lazy_gettext('Sur Name'),
        render_kw={
            "placeholder": "...",
            "data-position": "bottom right"
        }
    )


class AuthData(ModelForm):
    """
    """
    phone = TelField(
        lazy_gettext('Phone'),
        validators=[DataRequired()],
        render_kw={
            "placeholder": "700000000",
            "data-position": "bottom right"
        }
    )
    email = EmailField(
        lazy_gettext('Email Address'),
        validators=[DataRequired()],
        render_kw={
            "placeholder": "email@example.com",
            "data-position": "bottom right"
        }
    )
    password = PasswordField(
        lazy_gettext('Password'),
        validators=[DataRequired()]
    )

    def validate_email(self, field):
        """
        """
        if Users.query.filter_by(email=field.data).first():
            raise ValidationError(
                lazy_gettext('This email is already registered.')
            )

    def validate_phone(self, field):
        """
        """
        if Users.query.filter_by(phone=field.data).first():
            raise ValidationError(
                lazy_gettext('This phone is already registered.')
            )

