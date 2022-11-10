FROM python:3.9-alpine
ENV PYTHONBUFFERED 1

WORKDIR /banking_system
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD python manage.py runserver 0.0.0.0:80