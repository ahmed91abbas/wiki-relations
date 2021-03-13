DOCKER_IMAGE = relations-finder
COMMAND?=find-relations


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

.PHONY: run
run: build
	mkdir -p outdata
	touch $(realpath ./outdata)/spacy.html
	docker run --rm \
		-v $(realpath ./outdata)/spacy.html:/src/spacy.html \
		${DOCKER_IMAGE} local_runner.py ${COMMAND}
