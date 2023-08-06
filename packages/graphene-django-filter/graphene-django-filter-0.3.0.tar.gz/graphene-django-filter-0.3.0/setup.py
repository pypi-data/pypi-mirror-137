# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['graphene_django_filter']

package_data = \
{'': ['*']}

install_requires = \
['Django==3.2',
 'django-filter>=21.1,<22.0',
 'graphene-django>=2.15.0,<3.0.0',
 'graphene==2.1.9']

setup_kwargs = {
    'name': 'graphene-django-filter',
    'version': '0.3.0',
    'description': 'Advanced filters for Graphene',
    'long_description': '# graphene-django-filter\nAdvanced filters for Graphene.\n',
    'author': 'devind-team',
    'author_email': 'team@devind.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/devind-team/graphene-django-filter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2',
}


setup(**setup_kwargs)
