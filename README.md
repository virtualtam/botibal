# Botibal

An XMPP bot that uses the SleekXMPP Python library

## Dependencies
* python2
* sleekxmpp

## Installation
virtualenv2 ENV
source ENV/bin/activate
pip install -r requirements.txt

## Configuration
Copy `config.py.example` to `config.py`, and customize connection values:
* nickname
* Jabber ID (JID)
* Room/Groupchat address
* admin JID (to control the bot)

## Usage
./fire_bal.py  [-h] [-d] (-b | -m | -q)

optional arguments:
  -h, --help       show this help message and exit
  -d, --debug      set logging to DEBUG
  -b, --botibal    BotiBal, the Fukung-addict bot
  -m, --minibal    MiniBal, the minimalist bot
  -q, --quizzibal  QuizziBal, the quizzical bot

## Available commands
Once the bot is online and connected to a groupchat, you can:
* get help for MUC commands
 * list all available commands
   `<bot_nick>: -h`
 * get help for a given command
   `<bot_nick>: <command> -h`
* execute MUC commands
  `<bot_nick>: command [args]`
* get help for PM commands
 * list all available commands
  `-h`
 * get help for a given command
   `<command> -h`
* execute PM commands
  `command [args]

The available commands depend on which bot is running, and are split as follows:
* MUC: command execution (say/display something)
* PM: bot admin
 * add, delete and list elements
 * change bot status
 * execute "hidden" MUC commands
