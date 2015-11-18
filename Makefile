PACKAGE=botibal
NPROC := $(shell nproc)
PYTHONFILES := $(shell find . -name '*.py')

all: lint coverage

clean:
	@rm -rf build dist
	@find . -name "*.pyc" -delete

distclean:
	@git clean -xdf

# setuptools
sdist: clean
	@python setup.py sdist

build: clean
	@python setup.py build

install: build
	@python setup.py install

# static analysis
lint: isort pep8 pep257 pylint

isort: clean
	@echo "=== isort ==="
	@isort $(PYTHONFILES) --check-only

pep%: clean
	@echo "=== PEP$* ==="
	@pep$* $(PYTHONFILES)

pylint: clean
	@echo "=== Pylint ==="
	@pylint -j $(NPROC) $(PYTHONFILES)

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
