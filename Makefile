.DEFAULT_GOAL := help
CODE = tinvest tests

.PHONY: all venv test lint format build docs update help clean mut

all: format lint test build docs clean

help:
	@echo 'Usage: make [target] ...'
	@echo ''
	@echo '    make all'
	@echo '    make format'
	@echo '    make lint'
	@echo '    make test'
	@echo '    make mut'
	@echo '    make build'
	@echo '    make docs'
	@echo '    make clean'
	@echo ''

venv:
	python -m venv .venv

update:
	poetry update

test:
	pytest --verbosity=2 --showlocals --strict --log-level=DEBUG --cov=$(CODE) $(args)

lint:
	flake8 --jobs 1 --statistics --show-source $(CODE)
	pylint --jobs 1 --rcfile=setup.cfg $(CODE)
	black --skip-string-normalization --line-length=88 --check $(CODE)
	pytest --dead-fixtures --dup-fixtures
	mypy $(CODE)
	safety check --full-report

format:
	autoflake --recursive --in-place --remove-all-unused-imports $(CODE)
	isort --apply --recursive $(CODE)
	black --skip-string-normalization --line-length=88 $(CODE)
	unify --in-place --recursive $(CODE)

docs:
	mkdocs build -s -v

build:
	poetry build

clean:
	rm -rf site || true
	rm -rf dist || true

mut:
	mutmut run
