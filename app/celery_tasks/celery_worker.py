from  celery import Celery


from .. import create_app
from ..config import Config

# app = create_app('development')

# celery_app = Celery(app.import_name)
# celery_app.set_default()
# celery_app.conf.update(Config.CELERY_CONFIG)
# celery_app.autodiscover_tasks()

# with app.app_context() as ctx:
#     ctx.push()
