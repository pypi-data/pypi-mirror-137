# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mapa']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0',
 'geojson>=2.5.0,<3.0.0',
 'haversine>=2.5.1,<3.0.0',
 'ipdb>=0.13.9,<0.14.0',
 'ipyleaflet>=0.14.0,<0.15.0',
 'matplotlib>=3.5.0,<4.0.0',
 'notebook>=6.4.6,<7.0.0',
 'numba>=0.54.1,<0.55.0',
 'numpy-stl>=2.16.3,<3.0.0',
 'numpy>=1.20,<2.0',
 'pystac-client>=0.3.1,<0.4.0',
 'rasterio>=1.2.10,<2.0.0',
 'requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['dem2stl = mapa.cli:dem2stl', 'mapa = mapa.cli:mapa']}

setup_kwargs = {
    'name': 'mapa',
    'version': '0.1.0',
    'description': '🌍 Create 3d-printable STLs from satellite elevation data 🌏',
    'long_description': None,
    'author': 'Fabian Gebhart',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fgebhart/mapa',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
