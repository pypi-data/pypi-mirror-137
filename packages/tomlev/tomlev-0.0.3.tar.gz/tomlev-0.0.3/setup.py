# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tomlev']

package_data = \
{'': ['*']}

install_requires = \
['tomli>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'tomlev',
    'version': '0.0.3',
    'description': 'Tomlev - Open-source Python framework to manage environment variables',
    'long_description': '# Tomlev - Open-source Python framework to manage environment variables\n\n[![Latest Version](https://badgen.net/pypi/v/tomlev)](https://pypi.python.org/pypi/tomlev/)\n[![Tomlev CI/CD Pipeline](https://github.com/thesimj/tomlev/actions/workflows/main.yml/badge.svg)](https://github.com/thesimj/tomlev/actions/workflows/main.yml)\n[![Coverage Status](https://badgen.net/coveralls/c/github/thesimj/tomlev)](https://coveralls.io/github/thesimj/tomlev?branch=main)\n![Versions](https://badgen.net/pypi/python/tomlev)\n[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Alerts](https://img.shields.io/lgtm/alerts/g/thesimj/tomlev.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/thesimj/tomlev/alerts/)\n[![Code Quality](https://img.shields.io/lgtm/grade/python/g/thesimj/tomlev.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/thesimj/tomlev/context:python)\n[![License](https://img.shields.io/pypi/l/tomlev.svg)](LICENSE)\n[![Downloads](https://static.pepy.tech/personalized-badge/tomlev?period=total&units=international_system&left_color=black&right_color=green&left_text=Downloads)](https://pepy.tech/project/tomlev)\n\n### Motivation\n\nto be filled later...\n\n### Install\n\n```shell\n# pip\npip install tomlev\n```\n\n```shell\n# poetry\npoetry add tomlev\n```\n\n### Basic usage\n\nto be filled later...\n\n### Strict mode\n\nto be filled later...\n\n### Support\n\nif you like **Tomlev** give it a start ⭐ https://github.com/thesimj/tomlev\n\n### License\n\nMIT licensed. See the [LICENSE](LICENSE) file for more details.\n',
    'author': 'Mykola Bubelich',
    'author_email': 'm+github@bubelich.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/thesimj/tomlev',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
