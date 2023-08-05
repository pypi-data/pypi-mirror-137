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
    'version': '0.1.7',
    'description': 'Backend helper functions for ekata gateway processor',
    'long_description': "### Ekata Gateway Processor backend helper functions\n\n#### Create form id\n\nUse this function to create a form id from your backend, if successful it will return `form_id` and `created_on`.\n\n```python\n    from ekata_gateway_processor_helper import create_payment_form\n    from ekata_gateway_processor_helper.exceptions import (\n        InvalidAPIKeyException, InvalidProjectException, NoEnabledCurrencyException,\n        InvalidArgumentsException\n    )\n\n    try:\n        form_id, created_on = create_payment_form(\n            amount=int(Decimal(amount) * 100) # Always provide in atomic amount of fiat currency,\n            fiat_currency='USD',\n            project_id='',\n            api_key=''\n        )\n    except InvalidProjectException as e:\n        print(e.message)\n    except InvalidAPIKeyException as e:\n        print(e.message)\n    except NoEnabledCurrencyException as e:\n        print(e.message)\n    except InvalidArgumentsException as e:\n        print(e.arguments)\n```\n\n#### Verify payment payload\n\nUse this function to verify payment payload received after successful payment\n\n```python\n    from ekata_gateway_processor_helper import verify_payload\n    if verify_payload(\n        payload='' # payload received from frontend or webhook,\n        signature_secret='' #payment signature secret\n        ):\n        # Proceed with checkout, like send success message to frontend etc\n```\n",
    'author': 'EkataIO Wizard',
    'author_email': 'support@ekata.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.ekata.io/ekata-io-projects/ekata-gateway-processor-helper-python',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
