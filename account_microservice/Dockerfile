# Generated via docker init, simplified soon after

FROM python:3.12-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR .

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

COPY . .

EXPOSE 8081

RUN sed -i '281,285d' /usr/local/lib/python3.12/site-packages/django/core/management/base.py
ENTRYPOINT ["sh", "startup.sh"]