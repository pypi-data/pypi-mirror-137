# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['mathprimes']
setup_kwargs = {
    'name': 'mathprimes',
    'version': '1.0.0',
    'description': 'Well documented, super fast, prime number methods using mathematical algorithms.',
    'long_description': None,
    'author': 'GrandMoff100',
    'author_email': 'nlarsen23.student@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
