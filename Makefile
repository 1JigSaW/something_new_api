PY=python3

.PHONY: install install-dev up down dev migrate revision lint fmt type test worker pre-commit seed-challenges seed-meta

install:
	$(PY) -m pip install --upgrade pip
	$(PY) -m pip install -r requirements.txt

install-dev:
	$(PY) -m pip install -r requirements.txt

up:
	docker compose up -d db redis

down:
	docker compose down

dev:
	uvicorn main:app --host 0.0.0.0 --port 8000 --reload

migrate:
	alembic upgrade head

revision:
	alembic revision -m "$m"

lint:
	ruff check .

fmt:
	ruff format .
	ruff check . --fix

type:
	mypy app

test:
	pytest -q

worker:
	$(PY) -m app.worker.worker

seed-challenges:
	$(PY) -m app.tasks.seed_challenges

seed-meta:
	$(PY) -m app.tasks.seed_meta

pre-commit:
	pre-commit install
	pre-commit run --all-files


