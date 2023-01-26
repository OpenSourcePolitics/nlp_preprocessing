FROM python:3.8

ENV PYTHONUNBUFFERED 1

WORKDIR /nlp_preprocessing

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY resources_installation.py .
RUN python resources_installation.py

COPY . .

EXPOSE 8080

ENV PORT 8080

CMD flask run --host=0.0.0.0 -p $PORT