# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['xlaz']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'xlaz',
    'version': '0.4.0',
    'description': 'XLA utilities in pure Python',
    'long_description': '# xlaz\n',
    'author': 'Shawn Presser',
    'author_email': 'shawnpresser@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/shawwn/xla',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
