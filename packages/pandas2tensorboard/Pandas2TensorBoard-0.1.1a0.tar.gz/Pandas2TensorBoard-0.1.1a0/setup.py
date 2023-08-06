# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pandas2tensorboard', 'pandas2tensorboard.test']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.4.0,<2.0.0', 'tensorboard>=2.8.0,<3.0.0', 'torch>=1.10.2,<2.0.0']

extras_require = \
{'all': ['modin>=0.13.0,<0.14.0',
         'dask>=2022.1.1,<2023.0.0',
         'intake-omnisci>=0.1.0,<0.2.0'],
 'backend': ['dask>=2022.1.1,<2023.0.0', 'intake-omnisci>=0.1.0,<0.2.0'],
 'modin': ['modin>=0.13.0,<0.14.0']}

setup_kwargs = {
    'name': 'pandas2tensorboard',
    'version': '0.1.1a0',
    'description': 'Pandas DataFrames converted to TensorBoard Format',
    'long_description': None,
    'author': 'Anselm Hahn',
    'author_email': 'Anselm.Hahn@gmail.com',
    'maintainer': 'Anselm Hahn',
    'maintainer_email': 'Anselm.Hahn@gmail.com',
    'url': 'https://pypi.org/project/pandas2tensorboard/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
