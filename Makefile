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

migrate: 
	@echo "Running migrations..."
	docker-compose exec -T catalog python manage.py migrate

fixtures:
	@echo "Loading fixtures..."
	cd catalog
	docker-compose exec -T catalog sh -c "python manage.py loaddata fixtures/*.json"

