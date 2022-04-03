.PHONY: build run

build:
	docker-compose build
build-no-cache:
	docker-compose --no-cache build
run:
	docker-compose up
