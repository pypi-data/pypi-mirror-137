# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['indsl',
 'indsl.data_quality',
 'indsl.detect',
 'indsl.filter',
 'indsl.fluid_dynamics',
 'indsl.forecast',
 'indsl.not_listed_operations',
 'indsl.oil_and_gas',
 'indsl.regression',
 'indsl.resample',
 'indsl.signals',
 'indsl.smooth',
 'indsl.statistics',
 'indsl.ts_utils']

package_data = \
{'': ['*'], 'indsl.smooth': ['img/*'], 'indsl.statistics': ['img/*']}

install_requires = \
['PyWavelets>=1.2.0,<2.0.0',
 'cognite-sdk>=2.39.0,<3.0.0',
 'csaps>=1.1.0,<2.0.0',
 'kneed>=0.7.0,<0.8.0',
 'numba>=0.55.0,<0.56.0',
 'pandas>=1.3.5,<2.0.0',
 'pytest>=6.2.2,<7.0.0',
 'scikit-image>=0.19.0,<0.20.0',
 'scipy>=1.7.3,<2.0.0',
 'sklearn>=0.0,<0.1',
 'statsmodels>=0.13.1,<0.14.0',
 'typeguard>=2.13.3,<3.0.0']

setup_kwargs = {
    'name': 'indsl',
    'version': '3.1.1',
    'description': 'Industrial Data Science Library by Cognite',
    'long_description': None,
    'author': 'Gustavo Zarruk',
    'author_email': 'gustavo.zarruk@cognite.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
