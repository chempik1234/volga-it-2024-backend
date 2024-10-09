python manage.py makemigrations --noinput
python manage.py migrate api --noinput
python manage.py migrate --noinput
python manage.py migrate token_blacklist --noinput
python manage.py migrate api zero --fake --noinput
python manage.py migrate token_blacklist zero --fake --noinput
python manage.py migrate api --noinput
python manage.py migrate token_blacklist --noinput

python manage.py grpcrunserver 127.0.0.1:50051 &
gunicorn account_microservice.wsgi --bind=0.0.0.0:8081
# gunicorn account_microservice.wsgi --bind=0.0.0.0:8081
# python manage.py run_gunicorn --bind=0.0.0.0:8081
# echo "SUCCESSFUL LAUNCH!"