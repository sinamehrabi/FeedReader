#!/bin/sh

if [ "$MODE" = "web" ]; then
    sleep 2
    gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:${PORT:-8000}

elif [ "$MODE" = "worker" ]; then
    sleep 30
    celery -A src.celery_app worker -E -l INFO

elif [ "$MODE" = "beat" ]; then
    sleep 30
    celery -A src.celery_app beat -l INFO

elif [ "$MODE" = "test" ]; then
    pytest
    rm test.db

else
    echo "MODE env var is not set"
    exec "$@"
fi


