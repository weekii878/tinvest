
.PHONY: venv test lint format docs update

BIN ?= .venv/bin/

CODE = tinvest
ALL_CODE = tinvest tests

venv:
	python3 -m venv .venv
	$(BIN)pip install poetry
	$(BIN)poetry install

update:
	$(BIN)poetry update

test:
	$(BIN)pytest --verbosity=2 --showlocals --strict --log-level=DEBUG --cov=$(CODE) $(args)

lint:
	$(BIN)flake8 --jobs 4 --statistics --show-source $(ALL_CODE)
	$(BIN)pylint --jobs 4 --rcfile=setup.cfg $(CODE)
	$(BIN)black --skip-string-normalization --line-length=88 --check $(ALL_CODE)
	$(BIN)pytest --dead-fixtures --dup-fixtures
	$(BIN)mypy $(ALL_CODE)
	$(BIN)mkdocs build -s

format:
	$(BIN)autoflake --recursive --in-place --remove-all-unused-imports $(ALL_CODE)
	$(BIN)isort --apply --recursive $(ALL_CODE)
	$(BIN)black --skip-string-normalization --line-length=88 $(ALL_CODE)
	$(BIN)unify --in-place --recursive $(ALL_CODE)

docs:
	$(BIN)mkdocs build -s -v
