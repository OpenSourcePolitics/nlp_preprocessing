FROM python:3.8 AS builder

WORKDIR /nlp_preprocessing

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./main.py ./

COPY ./resources_installation.py ./

COPY ./stop_words.txt ./

RUN python resources_installation.py

RUN mkdir ./dist

COPY ./data_management ./data_management

COPY ./data ./data

RUN python ./main.py -f "/nlp_preprocessing/data/subset_raw_data.csv"

FROM python:3.8

WORKDIR /dist

COPY --from=builder ./nlp_preprocessing/dist/* ./