#!/usr/bin/env python2
'Setup script for Botibal'
from setuptools import setup

setup(
    name='botibal',
    version='0.7.1',
    description='The silly, quizzical XMPP bot',
    author='VirtualTam',
    author_email='virtualtam@flibidi.org',
    license='MIT',
    url='https://github.com/virtualtam/botibal',
    keywords='bot jabber xmpp quizz chat',
    packages=['botibal', 'botibal.client'],
    install_requires=[
        'dnspython==1.12.0',
        'pyasn1==0.1.7',
        'pyasn1-modules==0.0.5',
        'sleekxmpp==1.3.1'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Topic :: Communications :: Chat'
    ])
