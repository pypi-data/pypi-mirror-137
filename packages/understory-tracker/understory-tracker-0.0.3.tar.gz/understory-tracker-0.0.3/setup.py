# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['understory', 'understory.apps.tracker', 'understory.apps.tracker.templates']

package_data = \
{'': ['*']}

install_requires = \
['understory>=0,<1']

entry_points = \
{'web.apps': ['tracker = understory.apps.tracker:app']}

setup_kwargs = {
    'name': 'understory-tracker',
    'version': '0.0.3',
    'description': 'Personal tracker for your personal website.',
    'long_description': None,
    'author': 'Angelo Gladding',
    'author_email': 'self@angelogladding.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
