#!/usr/bin/env python3
"""
Setup script for Botibal
"""
import codecs
import os
import re

from setuptools import find_packages, setup


def get_long_description():
    """
    Reads the main README.rst to get the program's long description
    """
    with codecs.open('README.rst', 'r', 'utf-8') as f_readme:
        return f_readme.read()


def get_program_metadata(attribute):
    """
    Reads program metadata from the main package's __init__
    """
    with open(os.path.join('botibal', '__init__.py'), 'r') as f_init:
        return re.search(
            r'^__{attr}__\s*=\s*[\'"]([^\'"]*)[\'"]'.format(attr=attribute),
            f_init.read(), re.MULTILINE
        ).group(1)


setup(
    name=get_program_metadata('title'),
    version=get_program_metadata('version'),
    description="The silly, quizzical XMPP bot",
    long_description=get_long_description(),
    author=get_program_metadata('author'),
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
        'slixmpp==1.1',
    ],
    extras_require={
        'DNS': ['dnspython==1.12.0'],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Communications :: Chat',
    ])
