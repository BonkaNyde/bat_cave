# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from datetime import datetime
from flask import (
    current_app,
    flash,
    request
)
from flask_babel import gettext
from flask_login import current_user
from flask_socketio import disconnect
from itsdangerous import TimedSerializer as Serializer
from math import floor
from time import time
from ua_parser import user_agent_parser
from urllib.parse import (
    urlparse,
    urljoin
)
from werkzeug.user_agent import UserAgent
from werkzeug.utils import (
    secure_filename,
    cached_property
)

import functools, os, hashlib, mmap, io


class ParsedUserAgent(UserAgent):
    @cached_property
    def _details(self):
        """
        """
        return user_agent_parser.Parse(self.string)

    @property
    def platform(self):
        """
        """
        return self._details['os']['family']

    @property
    def browser(self):
        """
        """
        return self._details['user_agent']['family']

    @property
    def version(self):
        """
        """
        return '.'.join(
            part
            for key in ('major', 'minor', 'patch')
            if (part := self._details['user_agent'][key]) is not None
        )


def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        """
        """
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped


def flash_errors(form, category="warning"):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash(gettext(f"{getattr(form, field).label.text} - {error}"), category)


def stream_template(template_name, **context):
    """Creates a data stream to the template."""
    current_app.update_template_context(context)
    t = current_app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    rv.enable_buffering(5)
    return rv


def is_safe_url(target):
    """Determines if a url is safe."""
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def date_diff(date1, date2):
    """
    """
    # print((date1), (date2))
    result =  (date1 - date2).days
    # print(result)
    return floor(result/365.25)


def log(current_filename, message, level='info'):
    """Logs messages."""
    if current_app.debug:
        getattr(current_app.logger, level)(f'[** { current_filename } **] {message}')


def allowed_file(filename):
    """
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def process_file(file, folder_to_save:str):
    file_name = secure_filename(file.filename)
    if file and allowed_file(file_name):
        filename_, extension = os.path.splitext(file_name)
        # print(os.path.getsize(poster_filename))
        log(__name__, "[ file + extension] {file_name}, {extension}")
        hashed_file_name = hashlib.sha256(
            bytes(
                f'{file_name}-{time()}-{current_user}',
                'utf-8'
            )
        ).hexdigest() + extension
        file.filename = hashed_file_name
        if current_app.debug:
            log(__name__, f"[ + encrypted file name ] {file.filename}")
            log(__name__, f'[ + saving file ] {file.filename}')
        upload_dir = current_app.config['UPLOAD_DIR']
        save_path = os.sep + os.path.join(
            f"{current_app.config['UPLOAD_FOLDER']}{os.sep}{folder_to_save}",
            file.filename
        )
        file.save(
            os.path.join(
                f'{upload_dir}{os.sep}{folder_to_save}',
                file.filename
            )
        )
        if current_app.debug:
            log(__name__, f'[ Save path: {save_path} ]')
            log(__name__, f"[ encrypted (filename + ext) ] {file.filename}")
        return save_path
    raise RuntimeError(gettext('This file is not supported'))


def process_grade(admission_year):
    """
    """
    return f'{(datetime.now().year - admission_year) + 1}'


def generate_token(expiration=3600, salt=None, **kwargs):
    """Generates token authentication."""
    serializer = Serializer(
        current_app.secret_key, expiration,
        salt=salt or current_app.secret_key
    )
    data = dict()
    data.update(kwargs)
    return serializer.dumps(data)


def decode_token(token, salt=None):
    """Checks for validity of the passed token."""
    serializer = Serializer(
        current_app.secret_key,
        salt=salt or current_app.secret_key
    )
    try:
        data = serializer.loads(token)
    except:
        return False, data
    return True, data


class FileHandler:
    """
    """
    def __init__(self, file, mode='r', encoding='utf8'):
        """
        file : the file object.
        mode : the mode to open the file. ['r', 'w', 'a', 'rb', 'wb', 'ab']
        encoding : the encoding to use. ['utf8', ]
        """
        self.file = file
        self.mode = mode
        self.encoding = encoding

    def mmap_read_file(self, chunk:tuple=()):
        """
        """
        filename = self.file.filename
        with open(
            filename, mode=self.mode, encoding=self.encoding
        ) as file_obj:
            with mmap.mmap(
                file_obj.fileno(),
                length=0,
                access=mmap.ACCESS_READ
            ) as mmap_obj:
                mmap_obj.read()
    
    def gen_livestream(self):
        """
        """
        file = self.mmap_read_file()
        while True:
            if current_app.queue.qsize():
                frame = current_app.queue.get().split('base64,')[-1].decode('base64')
            else:
                frame = self.mmap_read_file()
            yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    def io_write_buffer(self, buffer):
        """
        """
        with open(
            self.file.filename,
            mode=self.mode,
            encoding=self.encoding
        ) as file_obj:
            file_obj.write(buffer)


def format_date_time():
    """_summary_
    """


class PushNotification:
    """_summary_
    """
    