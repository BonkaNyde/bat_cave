from flask import (
    flash, render_template
)

from ..extensions import login_manager

from . import blueprint

@blueprint.route('/login')
def login():
    """
    """
    return render_template('auth/login.html')



@login_manager.user_loader
def load_user(id:int):
    """
    """
    return id

