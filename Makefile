start:
	docker-compose up -d
up:
	docker-compose up
down:
	docker-compose down
stop:
	docker-compose stop
build:
	docker-compose build
migrate:
	docker exec -it python_container alembic upgrade head
enter_db:
	docker exec -it db_container psql --username=eye_of_hell --dbname=my_db
reset: down start migrate stop up

