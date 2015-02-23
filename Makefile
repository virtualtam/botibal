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

coverage: clean
	@echo "=== Coverage ==="
	@rm -rf htmlcov
	@coverage run --source=botibal -m unittest discover -s tests
	@coverage report
	@coverage html

lint: pylint pep8

pep8: clean
	@echo "=== PEP8 ==="
	@$(PEP8) $(PEP8FLAGS) $(PYTHONFILES) || exit 0

pylint: clean
	@echo "=== Pylint ==="
	@$(PYLINT) $(PYLINTFLAGS) $(PYTHONFILES) || exit 0

test: clean
	@python -m unittest discover -s tests

travis_coverage:
	@coverage run --source=botibal -m unittest discover -s tests
	@coverage report
