from flask import (
    flash, render_template, send_from_directory
)

from . import blueprint


from celery import shared_task


@shared_task
def add(x, y):
    return x + y


@blueprint.route('/')
def home():
    """
    """
    add.delay(2, 3)
    return render_template('home.html')


@blueprint.route('/favicon.ico')
def favicon():
    """
    """
    return send_from_directory('static', 'favicon.ico')


@blueprint.route('/manifest.json')
def manifest():
    """
    """
    return send_from_directory('static', 'manifest.json')


