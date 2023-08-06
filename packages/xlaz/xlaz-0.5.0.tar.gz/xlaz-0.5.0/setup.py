# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['xlaz',
 'xlaz.pb',
 'xlaz.pb.tensorflow.compiler.xla',
 'xlaz.pb.tensorflow.compiler.xla.service']

package_data = \
{'': ['*']}

install_requires = \
['tensorflow-checkpoint-reader>=0.1.2,<0.2.0']

setup_kwargs = {
    'name': 'xlaz',
    'version': '0.5.0',
    'description': 'XLA utilities in pure Python',
    'long_description': '# xlaz\n',
    'author': 'Shawn Presser',
    'author_email': 'shawnpresser@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/shawwn/xlaz',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
