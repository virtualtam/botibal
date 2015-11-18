#!/usr/bin/env python
"""
Setup script for Botibal
"""
import sys

from setuptools import find_packages, setup

if sys.version_info < (3, 0):
    XMPP = 'sleekxmpp==1.3.1'
else:
    XMPP = 'slixmpp==1.1'

setup(
    name='botibal',
    version='0.7.2',
    description="The silly, quizzical XMPP bot",
    author="VirtualTam",
    author_email='virtualtam@flibidi.org',
    license='MIT',
    url='https://github.com/virtualtam/botibal',
    keywords="bot jabber xmpp quizz chat",
    packages=find_packages(exclude=['tests.*', 'tests']),
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
