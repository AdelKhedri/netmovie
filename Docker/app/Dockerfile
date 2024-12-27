FROM python:alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFRED 1
ENV DJANGO_SUPERUSER_PASSWORD 'adel 1381'

RUN mkdir /app
WORKDIR /app

RUN pip install --upgrade pip
ADD ../../requirements.txt .
RUN apk update
RUN apk add --no-cache gcc python3-dev
RUN pip install -r requirements.txt --no-cache

CMD python manage.py makemigrations --noinput && \
    python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput && \
    python manage.py loaddata initial_fixture.json ;\
    python manage.py createsuperuser --user adel --email myemail@gmail.com --noinput ;\
    gunicorn -b 0.0.0.0:8000 netmovie.wsgi 
