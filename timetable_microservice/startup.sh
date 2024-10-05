python manage.py migrate --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput
gunicorn timetable_microservice.wsgi --bind=0.0.0.0:8083