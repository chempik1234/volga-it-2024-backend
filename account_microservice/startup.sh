python manage.py makemigrations --noinput
python manage.py migrate api --noinput
python manage.py migrate --noinput
python manage.py migrate token_blacklist --noinput
python manage.py migrate api zero --fake --noinput
python manage.py migrate token_blacklist zero --fake --noinput
python manage.py migrate api --noinput
python manage.py migrate token_blacklist --noinput
gunicorn account_microservice.wsgi --bind=0.0.0.0:8081
python manage.py grpcrunserver