from gevent import monkey
monkey.patch_all()


def run_app():
    from app import create_app
    return create_app('development')


app, celery = run_app()

@celery.task(bind=True)
def debug_task(self):
    "debug handler for celery"
    app.logger.log(1, msg=self.request)
