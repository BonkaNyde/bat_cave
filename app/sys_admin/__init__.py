"""
"""
from flask import  Blueprint

blueprint = Blueprint('sys_admin', __name__)

from . import forms, views
