release: python manage.py migrate
web: gunicorn settings.asgi -k uvicorn_worker.UvicornWorker
worker:  celery -A project worker --loglevel=info --concurrency=${WEB_CONCURRENCY:-4}
