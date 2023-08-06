# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['uniq_char']
setup_kwargs = {
    'name': 'uniq-char',
    'version': '0.1.0',
    'description': 'program to find q-ty of unique chars in string',
    'long_description': None,
    'author': 'Volodymyr Siabro',
    'author_email': 'siabrovova@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
