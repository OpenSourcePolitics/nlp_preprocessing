PWD=$(shell pwd)
USERNAME := quentinlp
IMAGE_NAME := nlp-preprocessing
REPO_NAME := nlp-repo
VERSION := latest
TAG := $(USERNAME)/$(REPO_NAME):$(VERSION)

local-installation:
	python resources_installation.py

build:
	docker build -t $(IMAGE_NAME) . --compress
	docker run --rm -dit --name nlp-preprocessing nlp-preprocessing /bin/bash
	docker cp nlp-preprocessing:/dist/subset_raw_data_preprocessed.csv $(PWD)/dist/subset_raw_data_preprocessed.csv
	docker cp nlp-preprocessing:/dist/word_frequency.json $(PWD)/dist/word_frequency.json
	docker stop nlp-preprocessing

push:
	@make build
	docker tag $(IMAGE_NAME) $(USERNAME)/$(REPO_NAME):$(VERSION)
	docker push $(TAG)
