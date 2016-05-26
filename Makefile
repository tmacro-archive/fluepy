-include env_make
NS = tmacro
VERSION ?= latest

REPO = fluepy
NAME = fluepy
INSTANCE = default

.PHONY: build push shell run start stop rm release

build:
	docker build -t $(NS)/$(REPO):$(VERSION) .

push:
	docker push $(NS)/$(REPO):$(VERSION)

shell:
	docker run --rm --name $(NAME)-$(INSTANCE) -i -t $(PORTS) $(VOLUMES) $(LINKS) $(ENV) $(EXTRA) $(SHELL_ARGS) $(NS)/$(REPO):$(VERSION) /bin/sh

run:
	docker run --rm --name $(NAME)-$(INSTANCE) $(PORTS) $(VOLUMES) $(LINKS) $(ENV) $(EXTRA) $(NS)/$(REPO):$(VERSION)

start:
	docker run -d --name $(NAME)-$(INSTANCE) $(PORTS) $(VOLUMES) $(ENV) $(EXTRA) $(NS)/$(REPO):$(VERSION)

stop:
	docker stop $(NAME)-$(INSTANCE)

rm:
	docker rm $(NAME)-$(INSTANCE)

squash:
	docker save $(NS)/$(REPO):$(VERSION) | sudo docker-squash -t $(NS)/$(REPO):$(VERSION) | docker load

release: build
	make squash -e VERSION=$(VERSION)
	make push -e VERSION=$(VERSION)

default: build
