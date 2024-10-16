python manage.py makemigrations
python manage.py migrate api
python manage.py migrate
python manage.py migrate api zero --fake
python manage.py migrate api
gunicorn timetable_microservice.wsgi --bind=0.0.0.0:8083