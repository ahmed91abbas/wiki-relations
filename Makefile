DOCKER_IMAGE = wiki-relations

# docker-compose related

.PHONY: up
up:
	docker-compose up -d --build

.PHONY: down
down:
	docker-compose down

.PHONY: logs
logs:
	docker-compose logs --follow

# supported commands

.PHONY: create-graph
create-graph:
	COMMAND=create-graph docker-compose up -d --build

.PHONY: clean-graph
clean-graph:
	COMMAND=clean-graph docker-compose up -d --build

.PHONY: find-relations
find-relations: build
	mkdir -p outdata
	touch $(realpath ./outdata)/spacy.html
	docker run --rm \
	-v $(realpath ./outdata)/spacy.html:/src/spacy.html \
	${DOCKER_IMAGE} main.py find-relations

# code related

.PHONY: build
build:
	docker build -t ${DOCKER_IMAGE} .

.PHONY: lint
lint: build
	docker run --rm \
		${DOCKER_IMAGE} -m flake8

.PHONY: test
test: build
	docker run --rm \
		-v $(realpath ./tests):/src/tests \
		${DOCKER_IMAGE} -m pytest tests
