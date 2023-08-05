# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fracdiff', 'fracdiff.sklearn', 'fracdiff.torch']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21.3,<2.0.0', 'scipy>=1.7.1,<2.0.0', 'statsmodels>=0.13.0,<0.14.0']

extras_require = \
{'scikit-learn': ['scikit-learn>=1.0.1,<2.0.0'],
 'torch': ['torch>=1.9.0,<2.0.0']}

setup_kwargs = {
    'name': 'fracdiff',
    'version': '0.7.1',
    'description': 'Super-fast fractional differentiation.',
    'long_description': None,
    'author': 'Shota Imaki',
    'author_email': 'shota.imaki.0801@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fracdiff/fracdiff',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.12,<3.10',
}


setup(**setup_kwargs)
