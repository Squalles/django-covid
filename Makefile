.PHONY: migrate tests

up:
	docker-compose up --build

down:
	docker-compose down

tests:
	docker-compose exec web pytest

migrate:
	docker-compose exec web python manage.py migrate

collectstatic:
	docker-compose exec web python manage.py collectstatic

fetchstats:
	docker-compose exec web python manage.py fetchstats
