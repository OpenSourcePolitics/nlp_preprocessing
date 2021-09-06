FROM python:3.8

ENV PYTHONUNBUFFERED=1\
PORT=8080\
FLASK_ENV=production

EXPOSE $PORT

WORKDIR /nlp_preprocessing

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN python resources_installation.py

CMD gunicorn --bind 0.0.0.0:$PORT --access-logfile - --error-logfile - --log-level debug wsgi:app