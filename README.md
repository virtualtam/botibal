# Botibal

[![Build Status](https://travis-ci.org/virtualtam/botibal.png?branch=master)](http://travis-ci.org/virtualtam/botibal)

A silly, quizzical XMPP bot based on the
[SleekXMPP](https://github.com/fritzy/SleekXMPP) (Python 2.7) and
[SliXMPP](https://dev.louiz.org/projects/slixmpp) (Python 3.4+) Python libraries.

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
$ botibal [-h] [-d] (-b | -m | -q) config_file

positional arguments:
  config_file      Configuration file

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

### Example: MUC interaction (MiniBal)
```
<Hans> plop Minibal
<Minibal> plop Hans
[...]
<Hans> Minibal: -h
<Minibal> 
usage: Minibal:  [-h] {say,time} ...

positional arguments:
  {say,time,taunt}
    say             say something
    time
[...]
<Hans> Minibal: say -h
<Minibal> 
usage: Minibal: say [-h] text [text ...]

positional arguments:
  text
[...]
<Hans> Minibal: say hello, world!
<Minibal> hello, world!
```

### Example: PM interaction (MiniBal)
```
<Hans> -h
<Minibal> 
usage: Minibal:  [-h] {say,time,quit,taunt} ...

positional arguments:
  {say,time,quit,taunt}
    say                 say something
    time
    quit                tells the bot to stop
    taunt               manage taunts
[...]
<Hans> taunt add programming, do you speak it, mofo?
<Hans> taunt --list
<Minibal>
1 - programming, do you speak it, mofo? (Hans)
```

## Installation
### From sources
Clone and `cd` to this repository, then run the following commands:
```bash
$ virtualenv <OPTIONS> <ENV>
$ source <ENV>/bin/activate
$ pip install -r requirements.txt
$ make install
```

## Configuration
Copy `config.ini.example` to `config.ini`, and customize connection values:
* nickname;
* Jabber ID (JID);
* Room/Groupchat address;
* admin JID (to control the bot);
* whether to use TLS or not (useful for self-signed certificates on personal servers).

## Development tools
### Test dependencies
* coverage,
* isort,
* pep257,
* pep8,
* pylint.
```bash
$ pip install -r tests/requirements.txt
```

### Test makefile
A Makefile is available with useful dev/test targets:

#### Static analysis
```bash
# run isort import checks:
$ make isort

# run PEP8 syntax checks:
$ make pep257

# run PEP8 syntax checks:
$ make pep8

# run pylint syntax checks:
$ make pylint

# run all syntax checkers:
$ make lint
```

#### Tests
```bash
# run all unitary tests
$ make test

# run all unit tests, generate an HTML coverage report
$ make coverage
# take a look at the report
$ <browser> htmlcov/index.html
```
