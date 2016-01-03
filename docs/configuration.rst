Configuration
=============

Botibal relies on a simple `INI`_ file to hold its configuration.
An `example configuration file`_ is provided in the sources.

.. _INI: https://en.wikipedia.org/wiki/INI_file
.. _example configuration file: https://github.com/virtualtam/botibal/blob/master/config.example.ini

Example configuration file
--------------------------

For the bot to work properly, a configuration file must be created:

* it can be located anywhere on the disk,
* it will be passed as a mandatory argument when running a bot (see :doc:`usage`),
* it holds connection and administration information (JIDs, MUC).

.. literalinclude:: ../config.example.ini
   :language: ini
   :caption: ``config.example.ini``
