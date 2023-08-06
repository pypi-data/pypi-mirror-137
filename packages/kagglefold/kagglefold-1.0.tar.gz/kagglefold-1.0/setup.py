# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kagglefold', 'kagglefold.alphafold', 'kagglefold.mmseqs']

package_data = \
{'': ['*']}

install_requires = \
['absl-py>=0.13.0,<0.14.0',
 'appdirs>=1.4.4,<2.0.0',
 'dm-haiku>=0.0.4,<0.0.5',
 'matplotlib==3.1.3',
 'numpy>=1.19.0,<2.0.0',
 'pandas>=1.3.3,<2.0.0',
 'py3Dmol>=1.7.0,<2.0.0',
 'requests>=2.26.0,<3.0.0',
 'tensorflow-cpu>=2.6.0,<3.0.0',
 'tqdm>=4.62.2,<5.0.0']

extras_require = \
{'alphafold': ['alphafold-kagglefold==1.0', 'jax>=0.2.20,<0.3.0']}

entry_points = \
{'console_scripts': ['kagglefold_batch = kagglefold.batch:main']}

setup_kwargs = {
    'name': 'kagglefold',
    'version': '1.0',
    'description': 'Making protein folding accessible in kaggle platform',
    'long_description': None,
    'author': 'Milot Mirdita',
    'author_email': 'milot.mirdita@mpibpc.mpg.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
