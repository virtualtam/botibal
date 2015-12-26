#!/usr/bin/env python
"""
Setup script for Botibal
"""
import codecs
import sys

from setuptools import find_packages, setup

if sys.version_info < (3, 0):
    XMPP = 'sleekxmpp==1.3.1'
else:
    XMPP = 'slixmpp==1.1'

with codecs.open('README.rst', 'r', 'utf-8') as f_readme:
    LONG_DESCRIPTION = f_readme.read()

setup(
    name='botibal',
    version='0.7.3',
    description="The silly, quizzical XMPP bot",
    long_description=LONG_DESCRIPTION,
    author="VirtualTam",
    author_email='virtualtam@flibidi.net',
    license='MIT',
    url='https://github.com/virtualtam/botibal',
    keywords="bot jabber xmpp quizz chat",
    packages=find_packages(exclude=['tests.*', 'tests']),
    data_files=[('config', ['config.example.ini'])],
    entry_points={
        'console_scripts': [
            'botibal = botibal.client.run:run',
        ],
    },
    install_requires=[
        'pyasn1==0.1.9',
        'pyasn1-modules==0.0.8',
        XMPP,
    ],
    extras_require={
        'DNS': ['dnspython==1.12.0'],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Communications :: Chat',
    ])
