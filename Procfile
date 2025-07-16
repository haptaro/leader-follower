web: gunicorn settings.wsgi --log-file -
release: python manage.py migrate
worker:  celery -A project worker --loglevel=info --concurrency=${WEB_CONCURRENCY:-4}
