# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crispy_forms_govuk',
 'crispy_forms_govuk.layout',
 'crispy_forms_govuk.templatetags']

package_data = \
{'': ['*'],
 'crispy_forms_govuk': ['static/js/*',
                        'templates/govuk/*',
                        'templates/govuk/layout/*',
                        'templates/govuk/snippets/*']}

install_requires = \
['django-crispy-forms>=1.9.0,<1.10.0', 'django>=3.0.0,<3.1.0']

setup_kwargs = {
    'name': 'crispy-forms-govuk',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
