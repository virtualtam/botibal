PACKAGE=botibal
PYTHONFILES := $(shell find . -name '*.py')

all: lint coverage

clean:
	@rm -rf build dist
	@find . -name "*.pyc" -delete

distclean:
	@git clean -xdf

botibal: clean
	@python2 setup.py sdist

# static analysis
lint: isort pep8 pep257 pylint

isort: clean
	@echo "=== isort ==="
	@isort $(PYTHONFILES) --check-only

pep%: clean
	@echo "=== PEP$* ==="
	@pep$* $(PYTHONFILES) || true

opep8: clean
	@echo "=== PEP8 ==="
	@$(PEP8) $(PEP8FLAGS) $(PYTHONFILES) || true

pylint: clean
	@echo "=== Pylint ==="
	@pylint $(PYLINTFLAGS) $(PYTHONFILES) || true

# testing
basic_coverage: clean
	@echo "=== Coverage ==="
	@coverage run --source=$(PACKAGE) -m unittest discover -s tests
	@coverage report

coverage: clean basic_coverage
	@rm -rf htmlcov
	@coverage html

test: clean
	@python -m unittest discover -s tests
