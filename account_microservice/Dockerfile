# Generated via docker init, simplified soon after

FROM python:3.12.2-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR .

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

COPY . .

EXPOSE 8081

ENTRYPOINT ["python", "manage.py", "makemigrations", "--noinput", "&&",
"python", "manage.py", "migrate", "--noinput", "&&",
"gunicorn", "account_microservice.wsgi", "--bind=0.0.0.0:8081"]