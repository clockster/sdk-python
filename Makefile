.PHONY: spec generate check test lint types operations

spec:
	python scripts/sync_spec.py

generate:
	python scripts/generate.py

operations:
	python scripts/check_operations.py

lint:
	ruff check .
	ruff format --check .

types:
	mypy

test:
	pytest -q

check: lint types test operations
