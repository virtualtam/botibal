PACKAGE=botibal
NPROC := $(shell nproc)
PYTHONFILES := \
	$(shell find . \
		-not -path "*build*" \
		-not -path "*docs*" \
		-not -path "*.tox*" \
		-name '*.py')

.PHONY: clean distclean
all: lint coverage sdist build

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

bdist_wheel: clean
	@python setup.py bdist_wheel

install: build
	@python setup.py install

# pypi
twine: sdist bdist_wheel
	@twine upload dist/* -s

test_twine: sdist bdist_wheel
	@twine upload dist/* -s -r pypitest --skip-existing

# sphinx documentation
sphinx_%: clean
	@cd docs && $(MAKE) $*

# static analysis
lint: isort pep8 pep257 pylint

isort: clean
	@echo "=== isort ==="
	@isort $(PYTHONFILES) --check-only --diff

pep%: clean
	@echo "=== PEP$* ==="
	@pep$* $(PYTHONFILES)

pylint: clean
	@echo "=== Pylint ==="
	@pylint -j $(NPROC) $(PYTHONFILES)

# testing
coverage: clean
	@echo "=== Coverage ==="
	@coverage run --source=$(PACKAGE) -m unittest discover -s tests
	@coverage report

coverage_html: clean coverage
	@rm -rf htmlcov
	@coverage html

test: clean
	@python -m unittest discover -s tests
