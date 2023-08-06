# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['malariagen_data']

package_data = \
{'': ['*']}

install_requires = \
['BioPython',
 'dask[array]',
 'fsspec',
 'gcsfs',
 'numba',
 'numpy',
 'pandas',
 'plotly',
 'scikit-allel',
 'scipy',
 'xarray',
 'zarr']

setup_kwargs = {
    'name': 'malariagen-data',
    'version': '1.0.1',
    'description': 'A package for accessing MalariaGEN public data.',
    'long_description': None,
    'author': 'Alistair Miles',
    'author_email': 'alistair.miles@sanger.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
