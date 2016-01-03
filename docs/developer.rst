Developer resources
===================

See also:

* :doc:`installation`
* :doc:`configuration`

Requirements
------------

To install *production* and *test* dependencies:

.. code-block:: bash

   (botibal) $ pip install -r requirements/tests.txt

To install *production*, *test* and *development* dependencies:

.. code-block:: bash

   (botibal) $ pip install -r requirements/development.txt

Tools
-----

Static analysis:

* `isort`_: check imports ordering & formatting;
* `PEP257`_: check doctsring formatting;
* `PEP8`_: miscellaneous language checks;
* `Pylint`_: all-in-one syntax checker.

Tests:
* `coverage`_;
* `unittest`_.

Make targets
^^^^^^^^^^^^^

A Makefile is available with useful dev/test targets:

Static analysis:

.. code-block:: bash

   # run isort import checks
   $ make isort
   
   # run PEP8 syntax checks
   $ make pep257
   
   # run PEP8 syntax checks
   $ make pep8
   
   # run pylint syntax checks
   $ make pylint
   
   # run all syntax checkers
   $ make lint

Tests:

.. code-block:: bash

   # run all unitary tests
   $ make test
   
   # run all unit tests, generate an HTML coverage report
   $ make coverage

   # take a look at the report
   $ <browser> htmlcov/index.html

Tox
^^^

Alternatively, if you have
`Tox`_ installed, as well as
both Python 2.7 and 3.4 interpreters available:

.. code-block:: bash

  # yup, it's that simple ;-)
  $ tox

.. _coverage: https://coverage.readthedocs.org/
.. _isort: https://github.com/timothycrosley/isort#readme
.. _PEP257: http://pep257.readthedocs.org
.. _PEP8: http://pep8.readthedocs.org
.. _Pylint: http://www.pylint.org/
.. _Tox: http://tox.readthedocs.org/en/latest/
.. _unittest: https://docs.python.org/3.4/library/unittest.html
