.PHONY: migrate tests

up:
	docker-compose up --build

down:
	docker-compose down

tests:
	docker-compose exec web pytest

fetchstats:
	docker-compose exec web python manage.py fetchstats
