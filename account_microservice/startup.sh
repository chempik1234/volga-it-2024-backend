python manage.py makemigrations ;
python manage.py migrate ;
python manage.py grpcrunserver 127.0.0.1:$GRPC_PORT_ACCOUNT & ;
gunicorn account_microservice.wsgi --bind=0.0.0.0:8081
# gunicorn account_microservice.wsgi --bind=0.0.0.0:8081
# python manage.py run_gunicorn --bind=0.0.0.0:8081
# echo "SUCCESSFUL LAUNCH!"