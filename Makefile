NAME=powerstrip-slowreq

all: build container

build:
	mkdir -p build/linux  && GOOS=linux  go build -o build/linux/$(NAME)
	mkdir -p build/darwin && GOOS=darwin go build -o build/darwin/$(NAME)

container:
	docker build -t powerstrip-slowreq .

.PHONY: build container