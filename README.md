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

## Available commands [WIP]
Some commands are available in the MUC, some via PM, some via PM for the admin
only...
The code is under heavy rewrite, which includes command/argument parsing.
Once this has been done, managing and using the bot will be much easier ;-)
