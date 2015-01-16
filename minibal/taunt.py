# -*- coding: utf-8 -*-
'I swear...'
import random

TAUNT_FILE = 'taunts.txt'


class Tauntionary(object):
    'A nice collection of charming sentences'
    def __init__(self, filepath=TAUNT_FILE):
        self.taunt_file = filepath
        self.taunts = []
        self.load_file()

    def add_taunt(self, taunt):
        'Adds a new taunt'
        self.taunts.append(taunt)
        self.save_file()

    def taunt(self):
        'You piece of...'
        return self.taunts[random.randint(0, len(self.taunts) - 1)]

    def load_file(self):
        'Loads taunts from the given file'
        try:
            with open(self.taunt_file) as f_taunts:
                self.taunts = f_taunts.read().splitlines()
        except IOError:
            print 'No file found'

    def save_file(self):
        'Saves taunts in a file'
        with open(self.taunt_file, 'w') as f_taunts:
            f_taunts.write('\n'.join(self.taunts))
