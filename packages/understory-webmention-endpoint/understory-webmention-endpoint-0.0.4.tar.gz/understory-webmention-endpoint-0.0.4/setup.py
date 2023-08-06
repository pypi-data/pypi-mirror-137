# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['understory',
 'understory.apps.webmention_endpoint',
 'understory.apps.webmention_endpoint.templates',
 'understory.apps.webmention_endpoint.templates.received']

package_data = \
{'': ['*']}

install_requires = \
['understory>=0,<1', 'webmention>=0,<1']

entry_points = \
{'web.apps': ['webmention_endpoint = understory.apps.webmention_endpoint:app']}

setup_kwargs = {
    'name': 'understory-webmention-endpoint',
    'version': '0.0.4',
    'description': 'A Webmention receiver/sender for the Understory framework.',
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
