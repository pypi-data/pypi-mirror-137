# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nemesis',
 'nemesis.resources',
 'nemesis.resources.elasticsearch',
 'nemesis.schemas',
 'nemesis.schemas.elasticsearch',
 'nemesis.scripts',
 'nemesis.templates',
 'nemesis.tests',
 'nemesis.tests.resources.elasticsearch']

package_data = \
{'': ['*']}

install_requires = \
['Click>=7.1,<7.2',
 'dacite>=1.6.0,<2.0.0',
 'deepdiff>=5.6.0,<6.0.0',
 'elasticsearch>=7.15.2,<8.0.0',
 'marshmallow>=3.14.1,<4.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'pytz>=2021.3,<2022.0',
 'requests>=2.26.0,<3.0.0',
 'rich>=10.14.0,<11.0.0']

entry_points = \
{'console_scripts': ['nemesis = nemesis.scripts.nemesis:cli']}

setup_kwargs = {
    'name': 'nemesis',
    'version': '0.0.7',
    'description': 'Tool for managing Elasticsearch resources as code',
    'long_description': None,
    'author': 'Infra',
    'author_email': 'infra@elastic.co',
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
