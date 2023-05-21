gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 2 --bind 0.0.0.0:5000 --access-logfile - --error-logfile - wsgi:app

// gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker --bind 0.0.0.0:5000 --access-logfile - wsgi:app

// celery -A wsgi.celery worker -E --logfile .celery-logfile.txt -P gevent --autoscale 1,4
// 