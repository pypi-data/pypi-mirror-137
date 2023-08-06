# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chancepy']

package_data = \
{'': ['*']}

install_requires = \
['pytz>=2020.1,<2021.0']

setup_kwargs = {
    'name': 'chancepy',
    'version': '0.1.3',
    'description': 'Random generator helper for Python',
    'long_description': '<img src="./logo.jpg" width="150" />\n\n# ChancePy\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Actions Status](https://github.com/kovrr/chancepy/workflows/CI/badge.svg)](https://github.com/kovrr/chancepy/actions)\n[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/kovrr/chancepy/edit/master/LICENSE)\n[![pypi](https://img.shields.io/pypi/v/chancepy?style=flat-square)](https://pypi.org/project/chancepy/)\n\n\nChancePy - Random generator helper for Python. Inspired by [ChanceJS](https://chancejs.com/index.html).\n\n## Installation\n\n### with pip\n`pip install chancepy`\n\n### with poetry\n`poetry add chancepy`\n\n## Usage\n\n```python\nfrom chancepy import Chance\n\n# Basic Methods\nrand_string = Chance.string()\nrand_guid = Chance.guid()\nrand_int = Chance.int(min=2, max=32)\nrand_letter = Chance.letter(casing=\'lower\')\nrand_char = Chance.character(pool=\'acegikmoqsuwy\')\nrand_domain = Chance.domain()\n\n\n# Utilities\nrand_choice = Chance.pickone([1, 2, 3])\nrand_2_choices = Chance.pickset([\'a\', \'b\', \'c\', \'d\'], 2)\n\n# Time\nrand_date_in_april = Chance.date(month=4)\nrand_year = Chance.year(mini=1990)\nrand_month_name = Chance.month(mode="full")\nrand_weekday = Chance.weekday(mode="short")\nrand_hour = Chance.hour()\nrand_min = Chance.minute()\nrand_second = Chance.second()\nrand_millisecond = Chance.millisecond()\nrand_timezone = Chance.timezone()\nrand_timestamp = Chance.timestamp()\n\n```\n\n## Contributing\nPRs are welcome!\n',
    'author': 'Nuni',
    'author_email': 'nuni@kovrr.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kovrr/chancepy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
