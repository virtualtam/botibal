# Botibal

[![Build Status](https://travis-ci.org/virtualtam/botibal.png?branch=master)](http://travis-ci.org/virtualtam/botibal)

A silly, quizzical XMPP bot that uses the [SleekXMPP](https://github.com/fritzy/SleekXMPP) Python library.

## Available bots
### MiniBal, the minimalist bot
* connects to a groupchat,
* answers to plopping: `<user>: plop <bot>` => `<bot>: plop <user>`,
* allows to taunt users! :smile:
* gives the current date and time.

### Botibal, the silly, Fukung-addict-bot
* all of MiniBal's features,
* stores links to fukung.net images,
* knows basic text ciphering (currently, ROT13).

### Quizzibal, the quizzical bot
* all of MiniBal's features,
* quizz sessions!
* quizz handling: start/stop, display scores, manage questions.

## Usage
```bash
$ ./fire_bal.py  [-h] [-d] (-b | -m | -q)

optional arguments:
  -h, --help       show this help message and exit
  -d, --debug      set logging to DEBUG
  -b, --botibal    BotiBal, the Fukung-addict bot
  -m, --minibal    MiniBal, the minimalist bot
  -q, --quizzibal  QuizziBal, the quizzical bot
```

## Available commands
Once the bot is online and connected to a groupchat, you can:
* get help for MUC commands
 * list all available commands:
   `<bot_nick>: -h`
 * get help for a given command:
   `<bot_nick>: <command> -h`
* execute MUC commands:
  `<bot_nick>: command [args]`
* get help for PM commands:
 * list all available commands:
  `-h`
 * get help for a given command:
   `<command> -h`
* execute PM commands:
  `command [args]`

The available commands depend on which bot is running, and are split as follows:
* MUC: command execution (say/display something);
* PM: bot admin:
 * add, delete and list elements,
 * change bot status,
 * execute "hidden" MUC commands.

## Dependencies
* python2,
* sleekxmpp,
* optional - DNS resolution, SSL/TLS verification:
 * dnspython,
 * pyasn1,
 * pyasn1-modules.

## Installation
```bash
$ virtualenv2 ENV
$ source ENV/bin/activate
$ pip install -r requirements.txt
```

## Configuration
Copy `config.py.example` to `config.py`, and customize connection values:
* nickname;
* Jabber ID (JID);
* Room/Groupchat address;
* admin JID (to control the bot);
* whether to use TLS or not (useful for self-signed certificates on personal servers).

## Development tools
### Test dependencies
* coverage,
* pep8,
* pylint.
```bash
$ pip install -r tests/requirements.txt
```

### Test makefile
A Makefile is available with useful dev/test targets:
```bash
# run PEP8 syntax checks:
$ make pep8

# run pylint syntax checks:
$ make pylint

# run both syntax checkers:
$ make lint

# run all unitary tests
$ make test

# run all unit tests, generate an HTML coverage report
$ make coverage
# take a look at the report
$ <browser> htmlcov/index.html
```
