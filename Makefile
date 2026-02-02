.PHONY: dev test lint fmt

dev:
	uvicorn evalops_lab.api:app --host 0.0.0.0 --port 8098 --reload

test:
	pytest -q

lint:
	ruff check .
	mypy src

fmt:
	ruff format .
