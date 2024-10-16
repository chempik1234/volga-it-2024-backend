python manage.py makemigrations
python manage.py migrate

python manage.py grpcrunserver 127.0.0.1:$GRPC_PORT_HOSPITAL &
gunicorn hospital_microservice.wsgi --bind=0.0.0.0:8082