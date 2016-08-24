Installation
============

Botibal is currently compatible with `Python`_ 3.4 and 3.5, and has been
tested on Linux.

.. _Python: https://www.python.org/

With pip (system-wide)
----------------------

The simplest way to install Botibal is with `pip`_:

.. code-block:: bash

  $ pip install botibal

.. _pip: http://pip.readthedocs.org/en/stable/quickstart/

With pip & virtualenv (recommended)
-----------------------------------

To install Botibal in a Python `virtualenv`_
(here with Python 3.5 as the default interpreter):

.. code-block:: bash

  # create a new virtualenv
  $ virtualenv /path/to/envs/botibal

  # activate the virtualenv
  $ source /path/to/envs/botibal/bin/activate

  # install botibal
  (botibal) $ pip install botibal

  # check which packages have been installed
  (botibal) $ pip freeze
  aiodns==1.0.1
  botibal==0.7.5
  pyasn1==0.1.9
  pyasn1-modules==0.0.8
  slixmpp==1.1

.. _virtualenv: http://docs.python-guide.org/en/latest/dev/virtualenvs/

To specify a Python interpreter:

.. code-block:: bash

  # create a new Python 3 virtualenv
  $ virtualenv -p /usr/bin/python3.4 /path/to/envs/botibal3

  # activate the virtualenv
  $ source /path/to/envs/botibal3/bin/activate

  # install botibal
  (botibal3) $ pip install botibal

  # check which packages have been installed
  (botibal3) $ pip freeze
  aiodns==1.0.0
  botibal==0.7.5
  pyasn1==0.1.9
  pyasn1-modules==0.0.8
  pycares==1.0.0
  slixmpp==1.1
  wheel==0.24.0


From the sources
----------------

To install Botibal from the latest source revision and install it in a dedicated
`virtualenv`_:

.. code-block:: bash

  # fetch the sources
  $ git clone https://github.com/virtualtam/botibal
  $ cd botibal

  # create and activate a new virtualenv
  $ virtualenv /path/to/botibal-src
  $ source /path/to/botibal-src/bin/activate

  # upgrade pip (required to read requirements attributes)
  (botibal-src) $ pip install -U pip

  # build and install
  (botibal-src) $ make install

  # check which packages have been installed
  (botibal3) $ pip freeze

  aiodns==1.0.0
  botibal==0.7.5
  pyasn1==0.1.9
  pyasn1-modules==0.0.8
  pycares==1.0.0
  slixmpp==1.1
  wheel==0.24.0
