# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ekata_gateway_processor_helper']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'ekata-gateway-processor-helper',
    'version': '0.1.0',
    'description': 'Backend helper functions for ekata gateway processor',
    'long_description': None,
    'author': 'EkataIO Wizard',
    'author_email': 'support@ekata.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
