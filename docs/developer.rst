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
* `PEP8`_: miscellaneous language checks;
* `pydocstyle`_: check doctsring formatting (formerly `PEP257`_);
* `Pylint`_: all-in-one syntax checker.

Tests:
* `coverage`_;
* `unittest`_.

Tox
^^^

Alternatively, if you have
`Tox`_ installed, as well as
both Python 3.4 and 3.5 interpreters available:

.. code-block:: bash

  # yup, it's that simple ;-)
  $ tox

.. _coverage: https://coverage.readthedocs.org/
.. _isort: https://github.com/timothycrosley/isort#readme
.. _PEP257: http://pep257.readthedocs.org
.. _PEP8: http://pep8.readthedocs.org
.. _pydocstyle: http://www.pydocstyle.org/en/latest/
.. _Pylint: http://www.pylint.org/
.. _Tox: http://tox.readthedocs.org/en/latest/
.. _unittest: https://docs.python.org/3.4/library/unittest.html
