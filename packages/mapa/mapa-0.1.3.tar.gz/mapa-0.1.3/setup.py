# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mapa']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0',
 'geojson>=2.5.0,<3.0.0',
 'haversine>=2.5.1,<3.0.0',
 'ipyleaflet>=0.15.0,<0.16.0',
 'notebook>=6.4.8,<7.0.0',
 'numba>=0.55.1,<0.56.0',
 'numpy-stl>=2.16.3,<3.0.0',
 'numpy>=1.21,<2.0',
 'pystac-client>=0.3.2,<0.4.0',
 'rasterio>=1.2.10,<2.0.0',
 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['dem2stl = mapa.cli:dem2stl', 'mapa = mapa.cli:mapa']}

setup_kwargs = {
    'name': 'mapa',
    'version': '0.1.3',
    'description': '🌍 Create 3d-printable STLs from satellite elevation data 🌏',
    'long_description': "# mapa 🌍\nCreate 3d-printable STLs from satellite elevation data\n\n\n## Installation\n```\npip install mapa\n```\n\n## Usage\nmapa uses numpy and numba under the hood to crunch large amounts of data in little time.\n\nmapa provides the following approaches for creating STL files:\n\n### 1. Using the mapa interactive map\nThe easiest way is using the `mapa` cli. Simply type\n```\nmapa\n```\nA [jupyter notebook](https://jupyter.org/) will be started with an interactive map. Follow the described steps by\nexecuting the cells to create a 3d model of whatever place you like.\n\n### 2. Using the dem2stl cli\nThe `dem2stl` cli lets you create a 3d-printable STL file based on your tiff file. You can run a demo computation to get\na feeling of how the output STL will look like:\n```\ndem2stl demo\n```\nIf you have your tiff file ready, you may run something like\n```\ndem2stl --input your_file.tiff --output output.stl --model-size 200 --z-offset 3.0 --z-scale 1.5\n```\nThe full list of options and their intention can be found with `dem2stl --help`:\n```\nUsage: dem2stl [OPTIONS]\n\n  🌍 Convert DEM data into STL files 🌏\n\nOptions:\n  --input TEXT          Path to input TIFF file.\n  --output TEXT         Path to output STL file.\n  --as-ascii            Save output STL as ascii file. If not provided, output\n                        file will be binary.\n  --model-size INTEGER  Desired size of the generated 3d model in millimeter.\n  --max-res             Whether maximum resolution should be used. Note, that\n                        this flag potentially increases compute time\n                        dramatically. The default behavior (i.e.\n                        max_res=False) should return 3d models with sufficient\n                        resolution, while the output stl file should be <= 200\n                        MB.\n  --z-offset FLOAT      Offset distance in millimeter to be put below the 3d\n                        model. Defaults to 4.0. Is not influenced by z-scale.\n  --z-scale FLOAT       Value to be multiplied to the z-axis elevation data to\n                        scale up the height of the model. Defaults to 1.0.\n  --demo                Converts a demo tif of Hawaii into a STL file.\n  --make-square         If the input tiff is a rectangle and not a square, cut\n                        the longer side to make the output STL file a square.\n  --version             Show the version and exit.\n  --help                Show this message and exit.\n```\n\n### 3. Using mapa as python library\nIn case you are building your own application you can simply use mapa's functionality as a within your application by importing the modules functions.\n```python\nfrom mapa import convert_tif_to_stl\n\npath_to_stl = convert_tif_to_stl(...)\n```\n\n## Changelog\n\nSee [Releases](https://github.com/fgebhart/mapa/releases).\n\n\n## Contributing\n\nContributions are welcome.\n",
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
