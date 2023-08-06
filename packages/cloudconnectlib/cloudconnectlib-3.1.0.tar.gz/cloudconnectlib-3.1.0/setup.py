# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cloudconnectlib',
 'cloudconnectlib.common',
 'cloudconnectlib.configuration',
 'cloudconnectlib.core',
 'cloudconnectlib.splunktacollectorlib',
 'cloudconnectlib.splunktacollectorlib.common',
 'cloudconnectlib.splunktacollectorlib.data_collection']

package_data = \
{'': ['*']}

install_requires = \
['PySocks>=1.7.1,<2.0.0',
 'decorator==5.1.1',
 'jinja2>=2.10.1,<4.0.0',
 'jsonpath-ng>=1.5.2,<2.0.0',
 'jsonschema>=4.4.0,<5.0.0',
 'munch>=2.3.2,<3.0.0',
 'requests>=2.27.1,<3.0.0',
 'solnlib>=4.6.0,<5.0.0',
 'splunk-sdk>=1.6,<2.0',
 'splunktalib==3.0.0',
 'splunktaucclib==6.0.0']

setup_kwargs = {
    'name': 'cloudconnectlib',
    'version': '3.1.0',
    'description': 'APP Cloud Connect',
    'long_description': None,
    'author': 'Addon Factory template',
    'author_email': 'addonfactory@splunk.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
