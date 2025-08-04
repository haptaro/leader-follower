release: python manage.py migrate
web: gunicorn settings.asgi -k uvicorn.workers.UvicornWorker
worker:  celery -A settings worker --loglevel=info --concurrency=${WEB_CONCURRENCY:-4}
