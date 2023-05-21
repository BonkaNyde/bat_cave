from celery import current_app

def log(current_filename, message, level='info'):
    """Logs messages."""
    # if current_app.debug:
    getattr(current_app.logger, level)(f'[** { current_filename } **] {message}')

