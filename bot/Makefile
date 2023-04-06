lint:
	python -m flake8 .
	python -m isort --check-only --profile black .
	python -m black . --check
interrogate:
	interrogate -vv .
format:
	python -m isort --profile black .
	python -m black .
run:
	make format
	make interrogate
	python main.py
