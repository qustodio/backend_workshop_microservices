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

clean:
	@echo "Removing containers..."
	docker-compose stop
	docker-compose rm

migrations:
	@echo "Building migrations..."
	docker-compose exec -T catalog python manage.py makemigrations
	docker-compose exec -T recommendator python manage.py makemigrations

migrate: 
	@echo "Running migrations..."
	docker-compose exec -T catalog python manage.py migrate
	docker-compose exec -T recommendator python manage.py migrate
	docker-compose exec -T accounts python manage.py migrate

fixtures:
	@echo "Loading fixtures..."
	docker-compose exec -T catalog sh -c "python manage.py loaddata catalog/fixtures/*.json"
	docker-compose exec -T accounts sh -c "python manage.py loaddata initial_users"
