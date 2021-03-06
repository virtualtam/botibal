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
* `pycodestyle`_: miscellaneous language checks (formerly `PEP8`_);
* `pydocstyle`_: check doctsring formatting (formerly `PEP257`_);
* `Pylint`_: all-in-one syntax checker.

Tests:

* `coverage`_;
* `pytest`_;
* `unittest`_.

Tox
^^^

Alternatively, if you have `Tox`_ installed, as well as a Python 3.5+
interpreter available:

.. code-block:: bash

  # yup, it's that simple ;-)
  $ tox

.. _coverage: https://coverage.readthedocs.org/
.. _isort: https://github.com/timothycrosley/isort#readme
.. _PEP257: http://pep257.readthedocs.org
.. _PEP8: http://pep8.readthedocs.org
.. _pycodestyle: https://pycodestyle.readthedocs.io/en/latest/
.. _pydocstyle: http://www.pydocstyle.org/en/latest/
.. _Pylint: http://www.pylint.org/
.. _pytest: https://docs.pytest.org/en/latest/
.. _Tox: http://tox.readthedocs.org/en/latest/
.. _unittest: https://docs.python.org/3.4/library/unittest.html
