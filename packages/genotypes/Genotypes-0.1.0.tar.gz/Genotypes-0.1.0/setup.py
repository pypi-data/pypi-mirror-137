# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['genotypes']
setup_kwargs = {
    'name': 'genotypes',
    'version': '0.1.0',
    'description': 'Cross genotypes of any size!',
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
