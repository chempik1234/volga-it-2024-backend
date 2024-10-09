python manage.py makemigrations --noinput
python manage.py migrate api --noinput
python manage.py migrate --noinput

python manage.py grpcrunserver 127.0.0.1:50052 &
gunicorn hospital_microservice.wsgi --bind=0.0.0.0:8082