python manage.py makemigrations --noinput
python manage.py migrate --noinput
gunicorn hospital_microservice.wsgi --bind=0.0.0.0:8082