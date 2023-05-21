from flask import (
    Blueprint, current_app
)

blueprint = Blueprint('main', __name__)

from flask_login import current_user
from datetime import datetime
from flask_wtf.csrf import generate_csrf  # noqa: E402
from flask_babel import (
    format_currency, format_date,
    format_datetime, format_decimal,
    format_number, format_percent,
    format_scientific, format_timedelta,
)  # noqa: E402

from . import forms, views
from .. import socs
from ..utils import (
    date_diff, log, process_grade
)
from ..config import Config


@blueprint.app_context_processor
def inject_variables_for_jinja():
    """
    """
    return dict(
        format_datetime=format_datetime,
        format_timedelta=format_timedelta,
        locales=Config.SUPPORTED_LANGUAGES,
        get_locale=views.get_locale,
        generate_csrf=generate_csrf,
        process_grade=process_grade,
        current_user=current_user,
        current_app=current_app,
        date_diff=date_diff,
        datetime=datetime,
        sum=sum,
        # perm=Config.WEBNOTI_SERVER_KEY,
        dir=dir
    )
