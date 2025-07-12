PROJECT ?= vaultgres

up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f

restart:
	docker compose down --remove-orphans
	docker compose up --build

prune:
	docker system prune -f --volumes

clean:
	docker compose down --rmi all --volumes --remove-orphans
	docker image prune -f
