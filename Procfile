web: gunicorn browsedocs.wsgi:application 
web: uvicorn browsedocs.asgi:application 
celery: celery -A browsedocs worker -l error 
beat: celery -A browsedocs beat --scheduler django_celery_beat.schedulers:DatabaseScheduler --loglevel=info
