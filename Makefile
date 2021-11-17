.PHONY: build run stop


build:
	@echo "Building docker image..."
	docker-compose build

run:
	@echo "Running docker compose locally..."
	docker-compose up -d

stop:
	@echo "Stopping local environment..."
	docker-compose stop

migrations:
	@echo "Running migrations..."
	docker-compose exec -T python manage.py makemigrations

migrate: 
	@echo "Running migrations..."
	docker-compose exec -T python manage.py migrate
