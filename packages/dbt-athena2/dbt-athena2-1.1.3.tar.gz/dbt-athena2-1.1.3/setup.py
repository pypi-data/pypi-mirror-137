# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'dbt'}

packages = \
['athena']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dbt-athena2',
    'version': '1.1.3',
    'description': 'Athena adapter for dbt platform',
    'long_description': None,
    'author': 'Duc Nguyen',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
