PWD=$(shell pwd)
USERNAME := quentinlp
IMAGE_NAME := nlp-preprocessing
REPO_NAME := nlp_repo_public_test
VERSION := latest
TAG := $(USERNAME)/$(REPO_NAME):$(VERSION)
PORT := 8080
REGION := fr-par
REGISTRY_ENDPOINT := rg.$(REGION).scw.cloud
REGISTRY_NAMESPACE := osp-internal-tools
REGISTRY_TAG := $(REGISTRY_ENDPOINT)/$(REGISTRY_NAMESPACE)/$(IMAGE_NAME):$(VERSION)

start:
	@make build
	@make run

local-installation:
	python resources_installation.py

build-local:
	docker build -t $(IMAGE_NAME) . --compress
	docker run --rm -dit --name nlp-preprocessing nlp-preprocessing /bin/bash
	docker cp nlp-preprocessing:/dist/nlp_preprocessing_output.json $(PWD)/dist/nlp_preprocessing_output.json
	docker stop nlp-preprocessing

run:
	docker run -it -e PORT=$(PORT) -p $(PORT):$(PORT) --rm $(REGISTRY_TAG)

push:
	@make build-local
	docker tag $(IMAGE_NAME) $(USERNAME)/$(REPO_NAME):$(VERSION)
	docker push $(TAG)

build:
	docker build -t $(IMAGE_NAME) . --compress --tag $(REGISTRY_TAG)

login:
	docker login $(REGISTRY_ENDPOINT) -u userdoesnotmatter -p $(TOKEN)

push-scw:
	docker push $(REGISTRY_TAG)

deploy:
	@make login
	@make build
	@make push-scw

test:
	pytest tests --cov=. --cov-fail-under=85 --cov-report term-missing

lint:
	pylint ./**/*.py

dep:
	pip install pylint
	pip install -r requirements.txt

dep3:
	pip3 install pylint
	pip3 install -r requirements.txt


