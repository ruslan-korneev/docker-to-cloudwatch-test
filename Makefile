ci: lint

lint:
	poetry run black .
	poetry run ruff check .
	poetry run mypy .
	poetry run isort .
