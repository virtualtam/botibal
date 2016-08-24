all: sdist build
.PHONY: clean distclean

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
