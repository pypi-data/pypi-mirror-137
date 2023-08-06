# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mocon']

package_data = \
{'': ['*']}

install_requires = \
['WTForms>=3.0.1,<4.0.0', 'pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'mocon',
    'version': '0.1.0',
    'description': 'Mocon is pluggable configuration management tool',
    'long_description': '# mocon\nMocon is pluggable configuration management tool\n',
    'author': 'ischaojie',
    'author_email': 'zhuzhezhe95@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ischaojie/mocon',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
