# -*- coding: utf-8 -*-
from collections import (
    OrderedDict, namedtuple
)
from datetime import datetime
from gettext import gettext
# from turtle import title
from flask import (
    flash, redirect, render_template,
    request, url_for, make_response, 
    session, jsonify, current_app, abort
)
# from flask_breadcrumbs import (
#     default_breadcrumb_root, register_breadcrumb
# )
from flask_login import (
    current_user, login_required,
    login_user, logout_user
)
# from flask_paginate import Pagination, get_page_parameter
import time
# from .forms import (
# )
from ..models import (
    Document
)
from ..utils import (
    flash_errors, is_safe_url, stream_template,
    process_file, log
)
from ..celery_tasks.tasks import send_email
from . import blueprint


def current_milli_time():
    """
    """
    return round(time.time() * 1000)


@blueprint.route('/manifest.json')
@login_required
def manifest():
    """
    """
    return current_app.send_static_file(f'pwa/manifest/sys_admin_manifest.json')

@blueprint.route('/service_worker.js')
@login_required
def service_worker():
    """
    """
    log(__name__, 'school service worker retruct function')
    return current_app.send_static_file('pwa/service_worker/teacher_service_worker.js')


@blueprint.before_request
def before_requests():
    if current_user.is_anonymous:
        return redirect(
            url_for('auth.login')
        )
    if current_user.is_authenticated and current_user.type == 'sys_admin':
        current_user.last_seen = datetime.utcnow()
        current_user.save()
        log(
            'sys_admin.views',
            f'id: {current_user.id}, user_type: {current_user.type}'
        )
    else:
        return redirect(
            url_for(f'{current_user.type}.dashboard')
        )


@blueprint.route('/')
# @login_required
def dashboard():
    context = dict(
        title=f'{current_user.name.title}\'s dashboard'
    )
    template = render_template(
        'dashboard.html',
        **context
    )
    response = make_response(template)
    return response

