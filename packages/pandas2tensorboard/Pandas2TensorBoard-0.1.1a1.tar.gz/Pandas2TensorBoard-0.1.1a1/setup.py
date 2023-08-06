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
    'version': '0.1.1a1',
    'description': 'Pandas DataFrames converted to TensorBoard Format',
    'long_description': '[![CI - Python Package](https://github.com/Anselmoo/pandas2tensorboard/actions/workflows/python-ci.yml/badge.svg)](https://github.com/Anselmoo/pandas2tensorboard/actions/workflows/python-ci.yml)\n[![codecov](https://codecov.io/gh/Anselmoo/pandas2tensorboard/branch/main/graph/badge.svg?token=NqLEIbDdGY)](https://codecov.io/gh/Anselmoo/pandas2tensorboard)\n[![PyPI](https://img.shields.io/pypi/v/pandas2tensorboard?logo=PyPi&logoColor=gold)](https://pypi.org/project/pandas2tensorboard/)\n\n# Pandas2TensorBoard\n\n`Pandas2TensorBoard` is a library for transforming the [pandas DataFrame][1]\ninto the data fomrat of [TensorBoard][2]. `Pandas2TensorBoard` relies on\n[torch utilities][3] for the data transformation.\n\n![_](example/example.png)\n\n## Installation\n\n- Regular installation via `pip`:\n\n  ```shell\n  pip install pandas2tensorboard\n  ```\n\n- With [modin][4] backend for `pandas`\n\n  ```shell\n  pip install pandas2tensorboard[modin]\n  ```\n\n- With [Dask][5] and [omnisci][6] support for `pandas`\n\n  ```shell\n  pip install pandas2tensorboard[backend]\n  ```\n\n- With [Dask][5] and [omnisci][6] support for `pandas` and [modin][4] backend for `pandas`\n\n  ```shell\n  pip install pandas2tensorboard[all]\n  ```\n\n## Usage\n\nCurrently the following types of export from `pandas` to `tensorboard` are\nsupported:\n\n- `pd.DataFrame` -> `scalars`\n- `pd.DataFrame` -> `scalars` with timestamp\n- `pd.DataFrame` -> `scatter` via hyperparameters\n\nFor initializing the `pandas2tensorboard` library, the current syntax of Torch\'s\n[tensorboard.SummaryWriter][7] is used.\n\n### Examples\n\n1. Exporting a regular `pd.DataFrame` to `tensorboard` by removing columns with `str`:\n\n   ```python\n   import seaborn as sns\n\n   from pandas2tensorboard import pandas2tensorboard as p2t\n\n   pt = p2t.Pandas2TensorBoard()\n   pt.regular_df(\n       sns.load_dataset("planets"),\n       label="planets",\n       remove_nan=True,\n       remove_str=True,\n   )\n   pt.close()\n   ```\n\n2. Exporting a `pd.DataFrame` with time column to `tensorboard`:\n\n   ```python\n   import seaborn as sns\n\n   from pandas2tensorboard import pandas2tensorboard as p2t\n\n   pt = p2t.Pandas2TensorBoard()\n   pt.timeseries_df(\n       sns.load_dataset("attention"),\n       time="score",\n       label="attention",\n       remove_nan=True,\n       remove_str=True,\n       time_convert=True,\n   )\n   pt.close()\n   ```\n\n   > The time column with name `score` is transformed into `float` with timestamp.\n\n3. Exporting a `pd.DataFrame` with hyperparameters to `tensorboard`:\n\n   ```python\n   import seaborn as sns\n\n   from pandas2tensorboard import pandas2tensorboard as p2t\n\n   pt = p2t.Pandas2TensorBoard()\n   pt.scatter_df(\n       sns.load_dataset("anagrams"),\n       x_axis="subidr",\n       group="anagrams",\n       remove_nan=True,\n       remove_str=True,\n   )\n   pt.close()\n   ```\n\n   > The `x-axis` corresponds to `hparam_dict`; the dataframe without column\n   > `x_axis="subidr"` corresponds to `metric_dict`.\n\n## Contributing\n\nPlease feel free to open an [issue][8] or create a [pull request][9]; see also [contributing][10].\n\n## License\n\nCheck [MIT][11]\n\n[1]: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html\n[2]: https://www.tensorflow.org/tensorboard/get_started\n[3]: https://pytorch.org/docs/stable/tensorboard.html\n[4]: https://modin.readthedocs.io/en/stable/\n[5]: https://dask.org/\n[6]: https://github.com/Quansight/intake-omnisci\n[7]: https://pytorch.org/docs/stable/_modules/torch/utils/tensorboard/writer.html#SummaryWriter\n[8]: https://github.com/Anselmoo/pandas2tensorboard/issues\n[9]: https://github.com/Anselmoo/pandas2tensorboard/pulls\n[10]: https://github.com/Anselmoo/pandas2tensorboard/blob/main/CONTRIBUTING.md\n[11]: https://github.com/Anselmoo/pandas2tensorboard/blob/main/LICENSE\n',
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
