# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['understory',
 'understory.apps.websub_endpoint',
 'understory.apps.websub_endpoint.templates',
 'understory.apps.websub_endpoint.templates.received',
 'understory.apps.websub_endpoint.templates.sent']

package_data = \
{'': ['*']}

install_requires = \
['understory>=0,<1', 'websub-temporary>=0,<1']

entry_points = \
{'web.apps': ['websub_endpoint = understory.apps.websub_endpoint:app']}

setup_kwargs = {
    'name': 'understory-websub-endpoint',
    'version': '0.0.4',
    'description': 'A WebSub publisher/subscriber for the Understory framework.',
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
