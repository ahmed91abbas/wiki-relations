.PHONY: up
up:
	docker-compose up -d --build

.PHONY: down
down:
	docker-compose down

.PHONY: logs
logs:
	docker-compose logs --follow

.PHONY: lint
lint:
	docker run --rm \
		-e RUN_LOCAL=true \
		-e VALIDATE_PYTHON_PYLINT=false \
		-e VALIDATE_PYTHON_FLAKE8=false \
		-e VALIDATE_PYTHON_BLACK=false \
		-e VALIDATE_PYTHON_ISORT=false \
		-v $(realpath ./):/tmp/lint \
		github/super-linter
