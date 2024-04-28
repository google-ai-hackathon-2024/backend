FROM python:3.8

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

# Install ffmpeg and libsndfile1 to en-decode audio file
RUN apt-get update
RUN apt-get install -y ffmpeg libsndfile1
RUN rm -rf /var/lib/apt/lists/*

# Install related pyhon libraries
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_APP=backend.py

ENV PYTHONUNBUFFERED=1

CMD ["flask", "run", "--host=0.0.0.0"]