PACKAGE=botibal
PEP8 = pep8
PEP8FLAGS = --count --statistics --max-line-length=80
PYLINT = pylint
PYLINTFLAGS = -rn --disable=locally-disabled
PYTHONFILES := $(shell find . -name '*.py')

all: lint coverage

clean:
	@find . -name "*.pyc" -delete

distclean:
	@git clean -xdf

botibal: clean
	@python2 setup.py sdist

# static analysis
lint: pylint pep8 isort

isort: clean
	@echo "=== isort ==="
	@isort $(PYTHONFILES) --check-only

pep8: clean
	@echo "=== PEP8 ==="
	@$(PEP8) $(PEP8FLAGS) $(PYTHONFILES) || exit 0

pylint: clean
	@echo "=== Pylint ==="
	@$(PYLINT) $(PYLINTFLAGS) $(PYTHONFILES) || exit 0

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
