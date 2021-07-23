PWD=$(shell pwd)
USERNAME := quentinlp
IMAGE_NAME := nlp-preprocessing
REPO_NAME := nlp_repo_public_test
VERSION := latest
TAG := $(USERNAME)/$(REPO_NAME):$(VERSION)

local-installation:
	python resources_installation.py

build:
	docker build -t $(IMAGE_NAME) . --compress
	docker run --rm -dit --name nlp-preprocessing nlp-preprocessing /bin/bash
	docker cp nlp-preprocessing:/dist/subset_raw_data_preprocessed.csv $(PWD)/dist/subset_raw_data_preprocessed.csv
	docker cp nlp-preprocessing:/dist/word_frequency_subset_raw_data_preprocessed.json $(PWD)/dist/word_frequency_subset_raw_data_preprocessed.json
	docker cp nlp-preprocessing:/dist/word_frequency_subset_raw_data.json $(PWD)/dist/word_frequency_subset_raw_data.json
	docker stop nlp-preprocessing

push:
	@make build
	docker tag $(IMAGE_NAME) $(USERNAME)/$(REPO_NAME):$(VERSION)
	docker push $(TAG)

test:
	pytest tests --cov=. --cov-fail-under=90

lint:
	pylint ./**/*.py

dep:
	pip install pylint
	pip install -r requirements.txt

dep3:
	pip3 install pylint
	pip3 install -r requirements.txt

