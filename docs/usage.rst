Usage
=====

Start the bot
-------------

Run with no arguments to get the help string:

.. code-block:: bash

  $ botibal [-h] [-d] (-b | -m | -q) config_file database_file
    
  positional arguments:
    config_file      configuration file
    database_file    data storage file
    
  optional arguments:
    -h, --help       show this help message and exit
    -d, --debug      set logging to DEBUG
    -b, --botibal    BotiBal, the silly bot
    -m, --minibal    MiniBal, the minimalist bot
    -q, --quizzibal  QuizziBal, the quizzical bot

To start MiniBal:

.. code-block:: bash

  $ botibal -m ~/botibal/config.ini ~/botibal/botibal.db


Chat commands
-------------

The available commands depend on which bot is running, and are split as follows:

* *MUC* - command execution (say/display something);
* *PM* - bot admin:

  * add, delete and list elements,
  * change bot status,
  * send instructions that will result in the bot sending messages to the MUC.

The bots' internal command interface is derived from `argparse`_, interaction
is thus very similar to running programs from the command-line 
(see the :doc:`examples` section).

.. _argparse: https://docs.python.org/3.4/library/argparse.html


Once the bot is online and connected to a groupchat, you can:

* get help for MUC commands

  * list all available commands:
    ``<bot_nick>: -h``
  * get help for a given command:
    ``<bot_nick>: <command> -h``

* execute MUC commands:
  ``<bot_nick>: command [args]``
* get help for PM commands:

  * list all available commands:
    ``-h``
  * get help for a given command:
    ``<command> -h``

* execute PM commands:
  ``command [args]``
