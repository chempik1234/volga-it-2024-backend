python manage.py migrate api zero --fake --noinput
python manage.py makemigrations --noinput
python manage.py migrate api --noinput
python manage.py migrate --noinput
python manage.py search_index --create -f
python manage.py search_index --populate -f
gunicorn document_microservice.wsgi --bind=0.0.0.0:8084