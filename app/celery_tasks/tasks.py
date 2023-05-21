import mimetypes
from celery import shared_task
from celery.contrib.abortable import AbortableTask
# from celery.contrib.migrate import migrate_task, migrate_tasks
# from celery.beat import 
from flask import current_app
from flask_mail import Message
from webnoti import send_notification
from socket import gaierror
from ..models import Users
from ..extensions import (
    mail,
    socket_io
)
from ..utils import log
# from ..cache.cache_manager import connected_user_cache


@shared_task(bind=True, name='task.send_email')
def send_email(self, subject:str, recepients:list, body:str=None, html:str=None, sender:str=None, attachments:list=None, **kwargs):
    """
    """
    log(__name__, 'sending mail')
    msg = Message(subject=subject, recipients=recepients, **kwargs)
    msg.body = body if body else None
    msg.html = html if html else None
    if sender:
        msg.sender = sender
    if attachments:
        for attachment_url in attachments:
            with current_app.open_resource(attachment_url) as file:
                log(__name__, 'adding attachment to mail...')
                attachment_mimetype:str = mimetypes.guess_type(attachment_url)[0]
                msg.attach(
                    attachment_url,
                    attachment_mimetype, file.read()
                )
                log(__name__, 'attachment added to mail.')
        log(__name__, 'finished adding attachments to mail.')
    # with mail.connect() as mail_conn:
    try:
        mail.send(msg)
        # log(__name__, f'recepient: {recepients[0]}')
        user = Users.query.filter_by(email=recepients[0]).first()
        # log(__name__,  f'user: {user}')
        if user:
            import time
            time.sleep(3)
            # user_sid = connected_user_cache.get_key(user.id)
            # # log(__name__,  f'user_sid: {user_sid}')
            # if user_sid:
            #     # log(__name__, f'emiting to {user_sid}')
            #     sio_send_to_user.delay('login', {'response':'ayeee'}, to=user_sid)
            #     # socket_io.emit('login', {'response':'ayeee'}, to=user_sid)
    except gaierror:
        log(__name__, 'email not sent, there was an issue with your internet connection')


@shared_task(bind=True, base=AbortableTask, name="task.add_two") # has no options for ['medium'] consideration.
def add_two():
    """
    """
    print('Added two.')
    return 'two added'


@shared_task(bind=True, name="task.sio_send_to_user")
def sio_send_to_user(self, event_name:str, payload:any=None, to:str=None, namespace:str=None):
    """
    """
    args = (event_name, payload)
    kwargs = {
        'to':to
    }
    if namespace is not None:
        kwargs.update('namespace', namespace)
    
    log(__name__, f"args: {args}, kwargs: {kwargs}")

    return socket_io.emit(*args, **kwargs)
    

@shared_task(bind=True, base=AbortableTask, name="task.sio_broadcast")
def sio_broadcast(self, event:str, payload:any, room:str, broadcast:bool=True, include_self:bool=False):
    """
    """
    return socket_io.emit(event, payload, room=room, broadcast=broadcast, include_self=include_self)
