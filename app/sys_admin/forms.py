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
    SelectField, SubmitField, SelectMultipleField, 
    PasswordField, StringField, FloatField,
    BooleanField, FieldList, HiddenField,
    FileField, Field, Flags, FormField,
    IntegerField, EmailField, SearchField,
    DateField, DateTimeField, DateTimeLocalField,
    DecimalField, TextAreaField, IntegerRangeField,
    TelField, TimeField, URLField, choices
)
from wtforms.validators import (
    DataRequired, NumberRange, EqualTo,
    IPAddress, MacAddress, Length, Optional,
    InputRequired, Regexp, URL, AnyOf, NoneOf
)
from sqlalchemy import (
    and_, any_, func
)
from sqlalchemy.orm import (
    aliased,join, outerjoin, session
)
from ..models import (
    Document, Users
)
from ..utils import log

