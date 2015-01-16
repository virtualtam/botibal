#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'Botibal: a silly jabber bot'
import re
import sys
from jabberbot import botcmd
from minibal.client import MiniBal
from minibal import fukung
import config


# pylint: disable=too-many-public-methods
class BotiBal(MiniBal):
    'A silly fukung-addict jabber bot'
    __fails = dict()


    def unknown_command(self, mess, cmd, args):
        if self.get_sender_username(mess) == self.nickname:
            return

        matches = re.search(fukung.REGEX, mess.getBody())
        if matches:
            fukung.append(matches)
            return

        return self.failsHandler(mess)

    def failsHandler(self, mess):
        'Handles "fail" events'
        matches = re.search('(' + self.nickname + r': )?fails add (\w+)',
                            mess.getBody())
        if matches:
            return self.failcount('add', matches.group(2))

        matches = re.search(
            '(' + self.nickname + r': )?fails( dump)? ?(\w+@\w+\.\w+)?',
            mess.getBody())
        if matches:
            if matches.group(3):
                if matches.group(2):
                    return self.failcount(matches.group(2),
                                          matches.group(3))

                return self.failcount('dump', matches.group(3))

            if matches.group(2):
                return self.failcount(matches.group(2), 'all')

        matches = re.search(
            '(' + self.nickname + r'(:|,)? )(failcount|fails|fail)\+\+',
            mess.getBody())
        if matches:
            return self.failcount('add', self.get_sender_username(mess))

        matches = re.search(
            '('+self.nickname+'(:|,)? )(failcount|fails|fail)--',
            mess.getBody())
        if matches:
            return self.failcount(
                'del', self.get_sender_username(mess))

        return None


    def failcount(self, method, user):
        'How many fails?'
        if method == 'dump' and self.__fails != None:
            if user == 'all':
                msg = 'Fails: \n'
                for i in self.__fails.keys():
                    msg += i +': %d\n' % (self.__fails[i])
                return msg
            else:
                msg = user +'\'s failcount: %d' % (self.__fails[user])
                if self.__fails[user] >= 5:
                    msg += ' \n'+user+' shall now use a new name'
                return msg
        else:
            if method == 'add' and user != 'all':
                if user in self.__fails:
                    self.__fails[user] += 1
                    return self.failcount('dump', user)
                else:
                    self.__fails[user] = 1
                    return self.failcount('dump', user)
            else:
                if method == 'del' and user != 'all':
                    if user in self.__fails and self.__fails[user] >= 1:
                        self.__fails[user] -= 1
                        return self.failcount('dump', user)
                    else:
                        return 'Error: failcount < 0 or unknown user'
                else:
                    return None

    @botcmd
    def fails(self, mess, args):
        'Displays fails'
        usrnm = str(self.get_sender_username(mess))
        if re.match('^_(.)*', args):
            return 'Do not try to unleash the infinite fury, {}!'.format(usrnm)

        return self.failcount('dump', 'all')

    @botcmd
    def _rot13(self, mess, args):
        'Returns passed arguments rot13ed'
        usrnm = str(self.get_sender_username(mess))
        return '{}: {}'.format(usrnm, args.encode('rot13'))


    @botcmd
    def _fshow(self, mess, args):
        'Gives an almost random image url from fukung'
        if args == 'dump':
            return fukung.read(method=args)

        return fukung.read()


if __name__ == '__main__':
    #dirty fix, but needed to use unicode…
    reload(sys)
    sys.setdefaultencoding("utf-8")
    BOT = BotiBal(config.JID, config.PASSWORD, 'Botibal', config.ADMIN_JID)
    BOT.serve_forever()
