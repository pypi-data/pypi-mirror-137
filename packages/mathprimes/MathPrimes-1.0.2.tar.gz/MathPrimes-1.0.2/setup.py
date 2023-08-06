# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['mathprimes']
setup_kwargs = {
    'name': 'mathprimes',
    'version': '1.0.2',
    'description': 'Well documented, super fast, prime number methods using mathematical algorithms.',
    'long_description': '# Primes\n\nAn implementation of prime number methods useful for programming.\n\nInlcuding `is_prime(47)  # -> True`, and `prime_factorization(8345)  # -> {1669: 1, 5: 1}`.\n\n\n## Installation\n\nUse `pip` or `poetry` or your other favorite package manager that supports installing packages from [PyPI](https://pypi.org)!\n\n```py\npip install mathprimes\n# Or\npoetry add mathprimes\n# Etc\n```\n\n## Usage\n```py\nfrom mathprimes import is_prime, prime_factorization\n```\n\n\n## Documentation\nSee `mathprimes.py` for function type hints, and function doc strings.\n\n',
    'author': 'GrandMoff100',
    'author_email': 'nlarsen23.student@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/GrandMoff100/MathPrimes',
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
