python manage.py makemigrations ;
python manage.py migrate ;
gunicorn timetable_microservice.wsgi --bind=0.0.0.0:8083