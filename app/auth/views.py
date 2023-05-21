import json
from flask import (
    abort, current_app, flash, make_response, session,
    redirect, render_template, request, url_for
)
from flask_babel import lazy_gettext, gettext
# from flask_breadcrumbs import (
#     default_breadcrumb_root, register_breadcrumb
# )
from flask_login import (
    current_user,
    fresh_login_required,
    login_required, 
    login_user, 
    logout_user
)
# from flask_paginate import Pagination, get_page_parameter
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from pip._vendor import cachecontrol
import google.auth.transport.requests as google_auth_request

from . import blueprint
from .forms import (
    ChangeEmailForm, 
    ChangePasswordForm, 
    LoginForm,
    ResetPasswordForm,
    ResetPasswordRequestForm
)

# from ..cache.cache_manager import (
#     flask_session_cache,
#     connected_user_cache,
#     disconnected_user_cache
# )

from ..celery_tasks.tasks import send_email
from ..extensions import login_manager
from ..models import Users, LoginHistory
from ..utils import (
    decode_token, flash_errors, generate_token, 
    is_safe_url, stream_template, log, ParsedUserAgent
)


@login_manager.user_loader
def load_user(user_id:int):
    """
    """
    user = Users.get_by_id(user_id)
    if user:
        return user.update(
            getattr(user, f'{user.type}s')
        )
    return None


def get_flow():
    """
    """
    flow = Flow.from_client_config(
        current_app.config.get('CLIENT_SECRETS_JSON'),
        scopes=[
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email",
            "openid"
        ],
        redirect_uri=current_app.config.get('GOOGLE_CB_REDIRECT_URI')
    )
    return flow


@blueprint.route('/google_OAuth_login')
def google_login():
    authorization_url, state = get_flow().authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@blueprint.route('/google_OAuth_cb')
def google_oauth_callback():
    """
    """
    flow = get_flow()
    flow.fetch_token(authorization_response=request.url)
    if not session.get('state') == request.args.get('state'):
        print(session.get('state'))
        abort(500)
    credentials = flow.credentials
    
    request_session = google_auth_request.requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google_auth_request.Request(session=cached_session)
    
    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=current_app.config.get('CLIENT_ID')
    )
    # auth_data = json.loads(id_info)
    user = Users.query.filter_by(email=id_info.get('email')).first()

    if current_app.debug:
        log(__name__, f"google id info: {id_info}")
    
    session['google_id'] = id_info.get("sub")
    session['name'] = id_info.get("name")
    if user is not None:
        user_data = getattr(user, f'{user.type}s')
        user.update(user_data)
        login_user(user, remember=True)
        task = send_email.delay(
            'Testing login notification',
            [user.email],
            body='just a test',
            html='<p>Wooyaaah.. im not clickable. click!</p>'
        )
        url = request.args.get('next') or url_for(f'{user.type}.dashboard')
        return redirect(url)
    flash(
        gettext(f'No user is registered for email {id_info.get("email")}')
    )
    return redirect(url_for('main.home'))


# @blueprint.route('/greeting')
# def greeting():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.index'))
#     return render_template('auth/greeting.html')

def manage_login(email_address, remember_cookie=False):
    """_summary_

    Args:
        user_agent (_type_): _description_
        remember_cookie (bool, optional): _description_. Defaults to False.

    Returns:
        _type_: _description_
    """
    user_agent:object = ParsedUserAgent(
        request.headers.get('User-Agent')
    )
    user = Users.query.filter_by(
        email=email_address
    ).first()
    log(__name__, user)
    log(__name__, user_agent)
    user_data = getattr(user, f'{user.type}s')
    user.update(user_data)
    loged_in_user = login_user(user, remember=remember_cookie)
    session_id = session.get('_id')
    login_history = LoginHistory()
    y = login_history.get(4)
    LoginHistory.get()
    current_session_history = login_history.get_session(session_id=session_id)
    if current_session_history:
        current_session_history.update({'remember_cookie': remember_cookie})
        log(__name__, f'session_history: {current_session_history.remember_cookie}')
    else:
        login_data = LoginHistory.create(
            user_id=user.id,
            platform=user_agent.platform,
            browser=user_agent.browser,
            remember_cookie=remember_cookie,
            session_sid=session.sid,
            session_id=session_id
        )
        log(__name__, f'login info: {login_data}')
    log(__name__, f'\nloged in user: {loged_in_user}, \nview_sid: {session.sid}, \n session _id: {session.get("_id")}')
    # send_email.delay(
    #     gettext('A device has logged in to your account'),
    #     [user.email],
    #     html=render_template('authentication/email/new_login.html', user_agent=user_agent, user=user)
    # )


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(
            url_for(f'{current_user.type}.dashboard')
        )
    form = LoginForm()
    context = {
        'form': form,
        'title': gettext('Login'),
    }
    if form.validate_on_submit():
        user_agent:object = ParsedUserAgent(
            request.headers.get('User-Agent')
        )
        user = Users.query.filter_by(
            email=form.email.data.strip()
        ).first()
        log(__name__, user)
        log(__name__, user_agent)
        if user is not None and user.verify_password(form.password.data):
            log(__name__, 'password verified')
            user_data = getattr(user, f'{user.type}s')
            user.update(user_data)
            loged_in_user = login_user(user, remember=form.remember.data)
            session_id = session.get('_id')
            current_session_history = LoginHistory.query.filter_by(session_id=session_id).first()
            if current_session_history:
                current_session_history.update({'remember_cookie': form.remember.data})
                log(__name__, f'session_history: {current_session_history.remember_cookie}')
            else:
                login_data = LoginHistory.create(
                    user_id=user.id,
                    platform=user_agent.platform,
                    browser=user_agent.browser,
                    remember_cookie=form.remember.data,
                    session_sid=session.sid,
                    session_id=session_id
                )
                log(__name__, f'login info: {login_data}')
            log(__name__, f'\nloged in user: {loged_in_user}, \nview_sid: {session.sid}, \n session _id: {session.get("_id")}')
            # send_email.delay(
            #     gettext('A device has logged in to your account'),
            #     [user.email],
            #     html=render_template('authentication/email/new_login.html', user_agent=user_agent, user=user)
            # )
            user_name = user.name if user.type=="school" else user.first_name + " " + user.last_name
            flash(gettext('Welcome ') + user_name)
            url = request.args.get('next') or url_for(f'{user.type}.dashboard')
            return redirect(url)
        flash(
            gettext(
                'Invalid username or password.'
            ),
            'error'
        )
    template = render_template('authentication/login.html', **context)
    response = make_response(template)
    return response


@blueprint.route('/signup')
def signup():
    """
    """
    context = {}
    template = render_template('authentication/signup.html', **context)
    response = make_response(template)
    return response


@blueprint.route('/logout')
@login_required
def logout():
    """
    """
    user = current_user

    name = user.name if user.type=='school' else user.first_name
    logout_user()
    flash(gettext('Good bye ') + name + '.', 'info')
    return redirect(url_for('main.home'))


@blueprint.route('/unconfirmed')
def unconfirmed():
    """
    """
    if not current_app.debug and not current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for(f'{current_user.type}.dashboard'))

    temp = render_template('authentication/unconfirmed.html')
    resp = make_response(temp)
    return resp


@blueprint.route('/confirm/<token>')
@login_required
def confirm(token):
    """
    """
    if current_user.confirmed:
        return redirect(
            url_for(f'{current_user.type}.dashboard')
        )
    if current_user.confirm_registration(token):
        flash(
            gettext('You have confirmed your account. Thanks!'),
            'success'
        )
        return redirect(
            url_for(f'{current_user.type}.dashboard')
        )
    flash(
        gettext('The confirmation link is invalid or has expired.'),
        'error'
    )
    return redirect(
        url_for('auth.resend_confirmation')
    )


@blueprint.route('/confirm')
@login_required
def resend_confirmation():
    """
    """
    if current_user.confirmed:
        return redirect(url_for('main.home'))
    token = current_user.generate_token()
    send_email.delay(
        gettext('Confirm your account'),
        [current_user.email],
        body=render_template('authentication/email/confirm.txt', user=current_user, token=token),
        html=render_template('authentication/email/confirm.html', user=current_user, token=token)
    )
    flash(
        gettext('A new confirmation email has been sent to you by email.'),
        'info'
    )
    if current_app.debug:
        return redirect(url_for('auth.confirm', token=token))
    return redirect(url_for('auth.unconfirmed', token=token))


@blueprint.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    """
    """
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_user.password = form.new_password.data
        current_user.save()
        current_user.update(password=form.new_password.data)
        flash(
            gettext('Your password has been updated.')
        )
        return redirect(request.args.get('next') or url_for('main.home'))
    temp = render_template(
        'authentication/forgot_password.html',
        form=form
    )
    resp = make_response(temp)
    return resp


@blueprint.route('/change_email', methods=['GET', 'POST'])
@fresh_login_required
def change_email():
    """
    """
    context = dict(
        title=gettext('Change Email Address')
    )
    form = ChangeEmailForm()
    if form.validate_on_submit():
        new_email = form.new_email.data.lower()
        token = current_user.generate_token(new_email=new_email)
        send_email.delay(
            'Confirm your new email',
            [new_email],
            body=render_template('auth/email/confirm_new_email.txt', user=current_user, token=token),
            html=render_template('auth/email/confirm_new_email.html', user=current_user, token=token)
        )
        flash(
            gettext('A confirmation email has been sent to your new email.'),
            'info'
        )
        return redirect(
            request.args.get('next') or url_for('main.home')
        )
        # return redirect(url_for("auth.confirm_new_email",token=token))
    temp = render_template('auth/change_email.html', form=form, **context)
    resp = make_response(temp)
    return resp


@blueprint.route('/change_email/<token>')
@login_required
def confirm_new_email(token):
    if current_user.confirm_new_email(token):
        flash(
            gettext('You have confirmed your new email. Thanks!'),
            'info'
        )
    else:
        flash(
            gettext('The confirmation link is invalid or has expired.'),
            'error'
        )
    return redirect(
        url_for('main.home')
    )


@blueprint.route('/reset_password', methods=['GET', 'POST'])
def reset_password_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.home'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(
            email=form.email.data.lower()
        ).first()
        token = user.generate_token()
        send_email.delay(
            recipients=[user.email],
            subject=gettext('Instructions to reset your password'),
            body=render_template(
                'auth/email/reset_password.txt',
                user=user,
                token=token
            ),
            html=render_template(
                'auth/email/reset_password.html',
                user=user,
                token=token
            )
        )
        flash(
            gettext('An email with instructions to reset password has been sent to you by email.'),
            'info'
        )
        return redirect(
            request.args.get('next') or url_for('auth.login')
        )
    temp = render_template('auth/reset_password.html', form=form)
    resp = make_response(temp)
    return resp


@blueprint.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if not current_user.is_anonymous:
        return redirect(
            url_for('main.dashboard')
        )
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(
            email=form.email.data.lower()
        ).first()
        if user.confirm_reset(token, form.password.data):
            flash(
                gettext('You have reset your password to new.')
            )
            return redirect(
                request.args.get('next') or url_for('auth.login')
            )
        else:
            flash(
                gettext('The confirmation link is invalid or has expired.'),
                'error'
            )
            return redirect(
                request.args.get('next') or url_for('auth.reset_password_request')
            )
    temp = render_template('auth/reset_password.html', form=form)
    resp = make_response(temp)
    return resp
