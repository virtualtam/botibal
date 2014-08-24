# -*- coding: utf-8 -*-
'Fukung interaction'
import random


BASE_URL = 'http://www.fukung.net/v/'
REGEX = r'http://(www\.)?fukung.net/v/(\d+)/(\w+)\.(\w+)'

def append(matchobject):
    'Adds a fukung link to the list'
    text = matchobject.group(2)+'/'+matchobject.group(3)+'.'\
           +matchobject.group(4)+'\n'
    with open('fukung.log', 'a') as f_ukung:
        f_ukung.write(text)


def read(method='rand'):
    'Returns a fukung URL'
    with open('fukung.log', 'r') as f_ukung:
        ids = f_ukung.readlines()

    if method == 'dump':
        urls = ''
        for fid in ids:
            urls += BASE_URL + fid
        return urls
    else:
        return BASE_URL +\
            ids[random.randint(0, len(ids))]

