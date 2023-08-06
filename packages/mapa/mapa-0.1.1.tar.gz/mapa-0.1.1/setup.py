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
    'version': '0.1.1',
    'description': '🌍 Create 3d-printable STLs from satellite elevation data 🌏',
    'long_description': "# mapa 🌍\nCreate 3d-printable STLs from satellite elevation data\n\n\n## Installation\n```\npip install mapa\n```\n\n## Usage\nmapa uses numpy and numba under the hood to crunch large amounts of data in little time.\n\n### 1. Using the dem2stl cli\nThe `dem2stl` cli lets you create a 3d-printable STL file based on your tiff file. You can run a demo computation to get a feeling of how the output STL will look like:\n```\ndem2stl demo\n```\nIf you have your tiff file ready, you may run something like\n```\ndem2stl --input your_file.tiff --output output.stl --model-size 200 --z-offset 3.0 --z-scale 1.5\n```\nFor more details on the different options, check out the [docs](TODO).\n\n### 2. Using the mapa interactive map\nIf you don't have a tiff file handy, you may simple select your favorite region using the `mapa` cli. Simply type\n```\nmapa\n```\nA jupyter notebook will be started with an interactive map. Follow the described steps by executing the cells to create a 3d model of whatever place you like.\n\n### 3. Using mapa as python library\nIn case you are building your own application you can simply use mapa's functionality as a within your application by importing the modules functions.\n```python\nfrom mapa import convert_tif_to_stl\n\npath_to_stl = convert_tif_to_stl(...)\n```\nRefer to the [docs](TODO) for more details.\n\n\n## Documentation\n[docs](TODO)\n",
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
