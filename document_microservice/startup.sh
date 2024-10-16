python manage.py migrate api zero --fake ;
python manage.py makemigrations ;
python manage.py migrate api ;
python manage.py migrate ;
python manage.py search_index --create -f ;
python manage.py search_index --populate -f ;
gunicorn document_microservice.wsgi --bind=0.0.0.0:8084