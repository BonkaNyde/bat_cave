FROM ubuntu:14.04

# copy source code
COPY . /flask-celery
WORKDIR /flask-celery

ENTRYPOINT celery -A celery_worker.worker.celery worker -E --logfile .celery-logfile.txt -P gevent --autoscale 1,4
