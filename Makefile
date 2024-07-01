up:
	docker compose -f docker-compose-local.yml up -d

down:
	docker compose -f docker-compose-local.yml down --remove-orphans

up_ci:
	docker compose -f docker-compose-ci.yml up -d

up_ci_rebuild:
	docker compose -f docker-compose-ci.yml up --build -d

down_ci:
	docker compose -f docker-compose-ci.yml down --remove-orphans