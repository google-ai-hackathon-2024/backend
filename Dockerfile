# Dockerfile, Image, Container

FROM python:3.8

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_APP=backend.py

ENV PYTHONUNBUFFERED=1

CMD ["flask", "run", "--host=0.0.0.0"]