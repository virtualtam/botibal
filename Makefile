PYLINT = pylint
PYLINTFLAGS = -rn --disable=locally-disabled
PYTHONFILES := $(wildcard *.py)

.PHONY: clean distclean coverage pylint test
all: clean distclean coverage pylint test

clean:
	@find . -name "*.pyc" -delete

distclean:
	@git clean -xdf

coverage: clean
	@rm -rf htmlcov
	@coverage run -m unittest discover -s tests
	@coverage html

pylint: clean
	@$(PYLINT) $(PYLINTFLAGS) $(PYTHONFILES) || exit 0

test: clean
	@python -m unittest discover -s tests
