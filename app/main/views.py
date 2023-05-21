# -*- coding: utf-8 -*-
import json, requests
from collections import (
    OrderedDict, namedtuple
)
from datetime import datetime
from gettext import gettext
from flask import (
    flash, redirect, render_template, request, url_for, 
    make_response, session, jsonify, current_app
)
# from flask_breadcrumbs import (
#     default_breadcrumb_root, register_breadcrumb
# )
from flask_login import (
    current_user, login_required, login_user, logout_user
)
# from flask_paginate import Pagination, get_page_parameter
import time
from .forms import (
    Users
)
from ..models import (
    Users
)
from . import blueprint
from ..celery_tasks.tasks import send_email, add_two
from ..extensions import babel
from ..utils import (
    flash_errors, is_safe_url,
    stream_template, process_file,
    log
)


# def is_endpoint_always_accessible():
#     return request.endpoint and (
#         request.endpoint[:5] == 'auth.' or
#         request.endpoint == 'main.set_locale' or
#         request.endpoint == 'static'
#     )


@blueprint.before_request
def before_requests():
    """
    """
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        current_user.save()
        log(__name__, f'id: {current_user.id}, user_type: {current_user.type}' )


# @blueprint.record_once
# def on_load(state):
#     """
#     http://stackoverflow.com/a/20172064/742173
#     :param state: state
#     """
#     state.app.login_manager.blueprint_login_views[
#         blueprint.name
#     ] = 'auth.login'


@babel.localeselector
def get_locale():
    """
    """
    locale = session.get('locale')
    if locale:
        log(__name__, f'[ babel locale ]: {locale}')
        return locale
    return request.accept_languages.best_match(
        current_app.config['SUPPORTED_LANGUAGES'].keys()
    )


@blueprint.route('/set_locale/<locale>')
def set_locale(locale):
    """
    """
    # locale = request.args.get(
    #     'locale', current_app.config['SUPPORTED_LANGUAGES'], type=str
    # )
    log(__name__, f"origin: {request.origin}")
    if locale in current_app.config['SUPPORTED_LANGUAGES'].keys():
        session['locale'] = locale
        log(__name__, f"Session Locale Set: {session.get('locale')}")
    else:
        session['locale'] = current_app.config['BABEL_DEFAULT_LOCALE']
    return session['locale']


@blueprint.route('/get_location')
def get_location():
    """
    """
    client_ip_address = request.remote_addr
    log(__name__, f'remote address: {client_ip_address}')
    url = f'http://ipinfo.io/{client_ip_address}/json'
    response = requests.get(url)
    log(__name__, f'ip info response: {response} - {response.text}.')
    rjs = json.loads(response.text)
    log(__name__, f'rjs: {rjs}')
    country = rjs.get('country')
    log(__name__, country)
    return country


@blueprint.route('/favicon.ico')
def favicon():
    """
    """
    return current_app.send_static_file('pwa/icons/favicon.ico')


@blueprint.route('/socket_worker.js')
@login_required
def message_worker():
    """
    """
    log(__name__, 'getting message_worker')
    return current_app.send_static_file('workers/socket_worker.js')



@blueprint.route('/')
def home():
    """
    """
    student_data = namedtuple('Student', ['student_id', 'cat1'])
    data = {
        "perfomance_data": [
            student_data(1, 80),
            student_data(2, 64),
            student_data(3, 39)
        ]
    }
    students = {
        1: 'harry thuku',
        2: 'david koira',
        3: 'rose nduta'
    }
    students = students
    context = dict(
        students = students,
        title = gettext('Home')
    ) 
    template = render_template('index.html', **context)
    response = make_response(template)
    # response['Content-Type'] = 'application/json'
    return response, 200


@blueprint.route('/messages', methods=['GET', 'POST'])
def messages():
    """_summary_

    Returns:
        _type_: _description_
    """
    title = 'Messages'
    template = render_template('messages.html', title=title)
    response = make_response(template)
    return response, 200


# @blueprint.route('/camera/<identity>/video_stream')
# def video_stream(identity):
#     camera = cv2.VideoCapture(identity)
#     return camera
