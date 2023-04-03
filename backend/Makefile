lint:
	python -m flake8 .
	python -m isort --check-only --profile black .
	python -m black . --check
test:
	coverage run --source='.' -m manage test
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
