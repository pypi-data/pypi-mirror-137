# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['masioware',
 'masioware.tools',
 'masioware.tools.mongo_flask_json_encoder',
 'masioware.tools.onion_requests',
 'masioware.tools.serializer',
 'masioware.tools.sqla_connection_builder']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.0.2,<3.0.0', 'bson>=0.5.10,<0.6.0', 'isodate>=0.6.1,<0.7.0']

setup_kwargs = {
    'name': 'masioware',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Marcio Martinez',
    'author_email': 'marcioedumartinez@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
