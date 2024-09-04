build:
	docker compose -f docker-compose.yml up --build -d --remove-orphans

up:
	docker compose -f docker-compose.yml up -d

down:
	docker compose -f docker-compose.yml down

down-v:
	docker compose -f docker-compose.yml down -v

show-logs:
	docker compose -f docker-compose.yml logs

show-logs-api:
	docker compose -f docker-compose.yml logs api

migrations:
	docker compose -f docker-compose.yml run --rm api python manage.py makemigrations

migrate:
	docker compose -f docker-compose.yml run --rm api python manage.py migrate

collectstatic:
	docker compose -f docker-compose.yml run --rm api python manage.py collectstatic --no-input --clear

superuser:
	docker compose -f docker-compose.yml run --rm api python manage.py createsuperuser

test:
	docker compose -f docker-compose.yml run --rm api python manage.py test