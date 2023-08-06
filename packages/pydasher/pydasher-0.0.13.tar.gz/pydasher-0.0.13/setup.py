# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pydasher']

package_data = \
{'': ['*']}

install_requires = \
['pydantic[dotenv]>=1.8.2,<2.0.0']

extras_require = \
{'docs': ['markdown-include==0.6.0',
          'mkdocs>=1.1.2,<2.0.0',
          'mkdocs-autorefs>=0.1.1,<0.2.0',
          'mkdocs-markdownextradata-plugin>=0.2.4,<0.3.0',
          'mkdocs-material>=7.0.6,<8.0.0',
          'mkdocstrings>=0.15.0,<0.16.0',
          'pdocs[docs]>=1.1.1,<2.0.0',
          'pymdown-extensions>=8.2,<9.0']}

setup_kwargs = {
    'name': 'pydasher',
    'version': '0.0.13',
    'description': 'A small set of utility functions for deterministically hashing pydantic base-models.',
    'long_description': None,
    'author': 'Michael Statt',
    'author_email': 'michael.statt@modelyst.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
