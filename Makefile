build:
	@docker-compose build
start:
	@docker-compose up
stop:
	@docker-compose down
logs:
	@docker-compose logs -f
shell:
	@docker-compose exec server /bin/bash