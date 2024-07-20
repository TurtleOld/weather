.PHONY: shell
shell:
		@poetry shell

.PHONY: install
install: .env
		@poetry install

.PHONY: start
start:
		@poetry run python manage.py runserver

.PHONY: poetry-export-requirements
poetry-export-requirements:
		@poetry export -f requirements.txt -o requirements.txt --without-hashes


.PHONY: up
up:
		@[ -f ./.env ] && \
			docker compose --env-file ./.env up -d || \
			docker compose up -d

.PHONY: down
down:
		@[ -f ./.env ] && \
			docker compose --env-file ./.env down || \
			docker compose down

.PHONY: migrate
migrate:
		poetry run python ./manage.py makemigrations && \
		echo "" && \
		echo "Migrating..." && \
		poetry run python ./manage.py migrate

.PHONY: setup
setup: migrate
		echo "Creating superuser '${DJANGO_SUPERUSER_USERNAME}' with password '${DJANGO_SUPERUSER_PASSWORD}' and email '${DJANGO_SUPERUSER_EMAIL}'" && \
		DJANGO_SUPERUSER_USERNAME="${DJANGO_SUPERUSER_USERNAME}" \
		DJANGO_SUPERUSER_PASSWORD="${DJANGO_SUPERUSER_PASSWORD}" \
		DJANGO_SUPERUSER_EMAIL="${DJANGO_SUPERUSER_EMAIL}" \
		poetry run python ./manage.py createsuperuser --noinput