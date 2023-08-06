# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['interactive_time_tracker']
setup_kwargs = {
    'name': 'interactive-time-tracker',
    'version': '0.1.0',
    'description': 'A tool to measure elapsed time of functions',
    'long_description': None,
    'author': 'Jéssica Meneguel',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
