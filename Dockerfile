FROM python:3.8

ENV PYTHONUNBUFFERED=1 \
PORT=8080 \
FLASK_ENV=production \
TIMEOUT=600

WORKDIR /nlp_preprocessing

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY resources_installation.py .
RUN python resources_installation.py

COPY . .

EXPOSE 8080

CMD gunicorn --bind 0.0.0.0:$PORT --access-logfile - --error-logfile - --log-level debug --timeout $TIMEOUT wsgi:app