python manage.py migrate --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput
gunicorn document_microservice.wsgi --bind=0.0.0.0:8084