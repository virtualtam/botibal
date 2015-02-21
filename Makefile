PYLINT = pylint
PYLINTFLAGS = -rn --disable=locally-disabled
PYTHONFILES := $(shell find . -name '*.py')

.PHONY: clean distclean coverage pylint test
all: clean distclean coverage pylint test

clean:
	@find . -name "*.pyc" -delete

distclean:
	@git clean -xdf

coverage: clean
	@rm -rf htmlcov
	@coverage run --source=botibal -m unittest discover -s tests
	@coverage html

pylint: clean
	@$(PYLINT) $(PYLINTFLAGS) $(PYTHONFILES) || exit 0

test: clean
	@python -m unittest discover -s tests
