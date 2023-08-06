# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fa_purity',
 'fa_purity.json',
 'fa_purity.json.errors',
 'fa_purity.json.primitive',
 'fa_purity.json.value',
 'fa_purity.pure_iter',
 'fa_purity.stream']

package_data = \
{'': ['*']}

install_requires = \
['Deprecated>=1.2.12,<2.0.0',
 'more-itertools>=8.10.0,<9.0.0',
 'simplejson>=3.17.6,<4.0.0',
 'types-Deprecated>=1.2.1,<2.0.0',
 'types-simplejson>=3.17.2,<4.0.0']

setup_kwargs = {
    'name': 'fa-purity',
    'version': '1.1.1',
    'description': 'Pure functional and typing utilities',
    'long_description': None,
    'author': 'Product Team',
    'author_email': 'development@fluidattacks.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
