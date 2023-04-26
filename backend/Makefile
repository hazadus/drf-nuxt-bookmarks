lint:
	python -m flake8 .
	python -m isort --check-only --profile black .
	python -m black . --check
test:
	coverage run --source='.' -m manage test bookmarks users downloads
	coverage html
interrogate:
	interrogate -vv .
format:
	python -m isort --profile black .
	python -m black .
run:
	make format
	make lint
	make test
	make interrogate
	python -m manage runserver
docker_test:
	docker compose up -d --build
	docker exec bkmrks-api coverage run --source='.' -m manage test bookmarks users downloads
	docker exec bkmrks-api coverage html
	docker compose down
up:
	make format
	make lint
	make interrogate
	docker compose up -d --build
	docker exec bkmrks-api coverage run --source='.' -m manage test bookmarks users downloads
	docker exec bkmrks-api coverage html
	docker compose logs --follow
down:
	docker compose down
reup:
	make down
	make up
functest:
	python -m manage test functests
docker_functest:
	docker compose up -d --build
	python -m manage test functests
	docker compose down