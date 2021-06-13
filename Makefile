test: lint acceptance-test
all: test build

PY3 = python3
POETRY = poetry

install:
	@echo "---- Installing package ---- "
	@$(POETRY) install

clean:
	@echo "---- Remove temporary files ---- "
	rm -rf .mypy_cache .pytest_cache dist

lint:
	@echo "---- Running type check and linter ---- "
	@$(POETRY) run mypy spotify_backup
	@$(POETRY) run black spotify_backup

acceptance-test:
	@echo "---- Running acceptance tests ---- "
	@$(POETRY) run pytest -ra -vv test/test_acceptance.py

build:
	@echo "---- Build distributable ---- "
	@$(POETRY) build

.PHONY: install all test acceptance-test build