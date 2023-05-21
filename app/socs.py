from flask import json, session, request
from flask_login import current_user, session_protected
# from flask_babel import gettext
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicKey
from flask_socketio import (
    emit, disconnect,
    join_room, send
)
from webnoti.notification import send_notification

# from tinyec import registry

# from .cache.cache_manager import (
#     app_cache, connected_user_cache,
#     disconnected_user_cache, flask_session_cache,
#     metrics_redis_cache, rq_cache
# )
from .celery_tasks.tasks import (
    sio_broadcast, sio_send_to_user
)
from .config import Config
from .extensions import socket_io
from .models import LoginHistory
from .utils import (
    authenticated_only, log
)


# @socket_io.on('connection')
# def connection():
#     """
#     """
#     log(__name__, 'connection')


def decode_flask_cookie(secret_key, cookie_str):
    import hashlib
    from itsdangerous import URLSafeTimedSerializer
    from flask.sessions import TaggedJSONSerializer
    salt = 'cookie-session'
    serializer = TaggedJSONSerializer()
    signer_kwargs = {
        'key_derivation': 'hmac',
        'digest_method': hashlib.sha1
    }
    s = URLSafeTimedSerializer(secret_key, salt=salt, serializer=serializer, signer_kwargs=signer_kwargs)
    return s.loads(cookie_str)


def notification_callback(resp_data):
    log(__name__, resp_data)
    return resp_data


# @authenticated_only
@socket_io.on('connect')
def connect():
    """
    """
    from flask import json
    # user_id:int = current_user.id
    session_id:str = session.get('_id')
    request_sid:str = request.sid
    from.config import Config
    log(__name__, decode_flask_cookie(Config.SECRET_KEY, session))
    # log(__name__, f'\nsession id: {session_id},\nsession accessed: {session.accessed}, \nsession permanent?: {session.permanent}, \nsession keys: {session.keys()}, \nsession values: {session.values()}, ')
    # disconnected_user:str = disconnected_user_cache.get_key(session_id)
    # if disconnected_user:
    #     disconnected_user_cache.delete_key(session_id)
    # connected_user_cache.set_key(session_id, request_sid)
    # log(__name__, connected_user_cache.get_key(session_id))
    # lotin_history = LoginHistory
    log(__name__, f'session id: {session_id}')
    current_session_ = LoginHistory.query.filter_by(user_id=current_user.id, session_id=session_id).first()
    log(__name__, f'push subscription: {current_session_.push_subscription}')
    send_notification(current_session_.push_subscription, 'json.dumps()', 'http://localhost:5001', Config.WEBNOTI_PRIVATE_KEY, notification_callback)

    # if not reply_to:
    #     connected_user_cache.set_key(
    #         str(user_id),
    #         request.sid #request.namespace #session['_id']
    #     )
    #     log(__name__, f'new user added. \nrequest_sid: {request.sid}, session_sid: {session.sid}')
    # fetch unread messages
    # messages = current_user.messages
    # fetch unread notifications
    # notifications = current_user.notifications
    # log(__name__, 'user exists')

    event_id = sio_send_to_user.delay(
        "message",
        {'msg': 'successful socketio connection'},
        to=request_sid
    )
    # log(__name__, f'event: {event_id}')
    # log(__name__, f"socketio user cache: {reply_to or 'No user found.'}")


# @authenticated_only
@socket_io.on('PING')
def ping(pong_data):
    log(__name__, 'pong event')
    current_user.ping()
    session_id:str = session.get('_id')
    # reply_to = connected_user_cache.get_key(session_id)
    # sio_send_to_user.delay('pong', {'msg': Config.WEBNOTI_SERVER_KEY}, to=reply_to)


# def add(a=5, b=5):
#     """
#     """
#     return a + b


@socket_io.on('push_notification_sub')
def push_noti_sub(subscription):
    """
    """
    # from .models import Users
    session_id = session.get('_id')
    login_history = LoginHistory.query.filter_by(user_id=current_user.id, session_id=session_id).first()
    sub = json.loads(subscription)
    log(__name__, f'all sessions: {login_history.id}')
    lh = LoginHistory()
    lh.get(LoginHistory.id)
    lh.update({'push_subscription': sub})
    # login_history.push_subscription = sub
    # login_history.save()
    log(__name__, f'push subscription: {lh.push_subscription}')
    notification = send_notification(lh.push_subscription, 'json.dumps()', 'https://google.com', Config.WEBNOTI_PRIVATE_KEY)
    return notification


@socket_io.on('get_perm')
def get_perm():
    """
    """
    return Config.WEBNOTI_SERVER_KEY


# @authenticated_only
@socket_io.on('disconnect')
def disconnect():
    log(__name__, 'user disconnected from socket')
    session_id = session.get('_id')
    sid = request.sid
    # connected_user_cache.delete_key(session_id)
    # disconnected_user_cache.set_key(session_id, sid)
    # room_id = rooms_sid[sid]
    # display_name = names_sid[sid]

    # print("[{}] Member left: {}<{}>".format(room_id, display_name, sid))
    # emit(
    #     "user-disconnect",
    #     {
    #         "sid": sid
    #     },
    #     broadcast=True,
    #     include_self=False,
    #     room=room_id
    # )

    # users_in_room[room_id].remove(sid)
    # if len(users_in_room[room_id]) == 0:
    #     users_in_room.pop(room_id)

    # rooms_sid.pop(sid)
    # names_sid.pop(sid)

    # print("\nusers: ", users_in_room, "\n")
    # socketio_user_cache = redis.from_url(f'{Config.REDIS_URL}/0')
    

# @socket_io.on('user_diconnect', namespace='/chat')
# @authenticated_only
# def handle_disconnects(reason):
#     socketio_user_cache.delete_key(current_user.id)
#     if reason:
#         log(__name__, f'[*socket*] User logged out {reason}.\n{socketio_user_cache.keys()}')


@socket_io.on_error()        # Handles the default namespace
def error_handler(e):
    log(__name__, e)
    # pass


# # @socketio.on_error('/chat') # handles the '/chat' namespace
# # def error_handler_chat(e):
# #     print('[#] Socket error, namespace="/chat"')
# #     pass


# # @socketio.on_error_default  # handles all namespaces without an explicit error handler
# # def default_error_handler(e):
# #     print('[#] Socket error. Default error message')
# #     pass

rooms_sid = {}
names_sid = {}
users_in_room = {}


# @socket_io.on("connect")
# def on_connect():
#     sid = request.sid
#     print("New socket connected ", sid)


@socket_io.on("join-room")
@authenticated_only
def on_join_room(data):
    sid = request.sid
    room_id = data["room_id"]
    display_name = f'uid_:{current_user.id}'

    # register sid to the room
    join_room(room_id)
    rooms_sid[sid] = room_id

    # broadcast to others in the room
    payload = {
        "sid": sid,
        "name": display_name
    }
    sio_broadcast.delay('user-connect', payload, broadcast=True, include_self=False, room=room_id)

    # add to user list maintained on server
    if room_id not in users_in_room:
        users_in_room[room_id] = [sid]
        socket_io.emit(
            "user-list",
            {
                "my_id": sid
            }
        )  # send own id only
    else:
        usrlist = {
            u_id: names_sid[u_id] \
                for u_id in users_in_room[room_id]
        }
        # send list of existing users to the new member
        emit(
            "user-list",
            {
                "list": usrlist,
                "my_id": sid
            }
        )
        # add new member to user list maintained on server
        users_in_room[room_id].append(sid)

    print("\nusers: ", users_in_room, "\n")


# @socket_io.on("data")
# def on_data(data):
#     sender_sid = data['sender_id']
#     target_sid = data['target_id']
#     if sender_sid != request.sid:
#         print("[Not supposed to happen!] request.sid and sender_id don't match!!!")

#     if data["type"] != "new-ice-candidate":
#         print('{} message from {} to {}'.format(
#             data["type"], sender_sid, target_sid))
#     socket_io.emit('data', data, room=target_sid)
