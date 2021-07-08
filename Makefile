USERNAME := quentinlp
IMAGE_NAME := nlp-preprocessing
REPO_NAME := nlp-repo
VERSION := latest
TAG := $(USERNAME)/$(REPO_NAME):$(VERSION)

local-installation:
	python resources_installation.py

build:
	docker build -t $(IMAGE_NAME) . --compress

push:
	@make build
	docker tag $(IMAGE_NAME)  $(USERNAME)/$(REPO_NAME):$(VERSION)
	docker push $(TAG)
