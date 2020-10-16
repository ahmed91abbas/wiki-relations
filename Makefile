.PHONY: up
up: setup
	docker-compose up -d

.PHONY: down
down: docker-compose down

.PHONY: setup
setup:
	mkdir -p $(realpath .)/neo4j

.PHONY: clean
clean:
	rm -r $(realpath .)/neo4j
