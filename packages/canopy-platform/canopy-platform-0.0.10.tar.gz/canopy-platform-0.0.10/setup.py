# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['canopy', 'canopy.static', 'canopy.templates']

package_data = \
{'': ['*']}

install_requires = \
['datrie>=0.8.2,<0.9.0',
 'numpy>=1.22.1,<2.0.0',
 'sounddevice>=0.4.4,<0.5.0',
 'understory-indieauth-client>=0,<1',
 'understory-indieauth-server>=0,<1',
 'understory-micropub-server>=0,<1',
 'understory-microsub-server>=0,<1',
 'understory-text-editor>=0,<1',
 'understory-text-reader>=0,<1',
 'understory-tracker>=0,<1',
 'understory-webmention-endpoint>=0,<1',
 'understory-websub-endpoint>=0,<1',
 'understory>=0,<1',
 'vosk>=0.3.32,<0.4.0',
 'waitress>=2.0.0,<3.0.0',
 'webvtt-py>=0.4.6,<0.5.0']

entry_points = \
{'console_scripts': ['build_gaea = gaea:build']}

setup_kwargs = {
    'name': 'canopy-platform',
    'version': '0.0.10',
    'description': 'Social web platform.',
    'long_description': '# Canopy\n\nSocial web platform\n\n![Demo](https://media.githubusercontent.com/media/canopy/canopy/main/demo.gif)\n\n## Use\n\n[Linux](https://github.com/canopy/canopy/releases/download/v0.0.1-alpha/gaea) |\nWindows |\nMac\n\n## Develop\n\n```shell\ngit clone https://github.com/canopy/canopy.git && cd canopy\n# manually remove relative dev dependencies from pyproject.toml\npoetry install\nWEBCTX=dev poetry run web serve canopy:app --port 9000\n# hack\npoetry run build_gaea  # optional\n```\n',
    'author': 'Angelo Gladding',
    'author_email': 'angelo@ragt.ag',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
