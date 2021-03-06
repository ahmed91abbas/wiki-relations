DOCKER_IMAGE = relations-viewer


.PHONY: build
build:
	docker build -t ${DOCKER_IMAGE} .

.PHONY: lint
lint: build
	docker run --rm \
		${DOCKER_IMAGE} lint

.PHONY: lint-fix
lint-fix: build
	docker run --rm \
		-v $(realpath ./src):/app/src \
		${DOCKER_IMAGE} lint:fix
