# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wraeblast',
 'wraeblast.filtering',
 'wraeblast.filtering.parsers.extended',
 'wraeblast.filtering.parsers.standard',
 'wraeblast.filtering.serializers']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.0.1,<4.0.0',
 'aiohttp>=3.7.4,<4.0.0',
 'backoff>=1.11.1,<2.0.0',
 'boto3>=1.18.26,<2.0.0',
 'cachetools>=4.2.2,<5.0.0',
 'cleo>=0.8.1,<0.9.0',
 'colorcet>=2.0.6,<3.0.0',
 'colormath>=3.0.0,<4.0.0',
 'colour>=0.1.5,<0.2.0',
 'glom>=20.11.0,<21.0.0',
 'inflection>=0.5.1,<0.6.0',
 'lark>=0.11.3,<0.12.0',
 'matplotlib>=3.4.2,<4.0.0',
 'mergedeep>=1.3.4,<2.0.0',
 'numpy>=1.22.2,<2.0.0',
 'palettable>=3.3.0,<4.0.0',
 'pandas>=1.3.2,<2.0.0',
 'pandera>=0.7.1,<0.8.0',
 'pydantic>=1.8.2,<2.0.0',
 'pydub>=0.25.1,<0.26.0',
 'python-json-logger>=2.0.1,<3.0.0',
 'requests>=2.25.1,<3.0.0',
 'ruamel.yaml>=0.17.5,<0.18.0',
 'structlog>=21.1.0,<22.0.0',
 'uplink[aiohttp]>=0.9.6,<0.10.0']

extras_require = \
{'tts': ['pyttsx3>=2.90,<3.0']}

entry_points = \
{'console_scripts': ['wraeblast = wraeblast.cmd:main']}

setup_kwargs = {
    'name': 'wraeblast',
    'version': '0.2.1',
    'description': 'Tools for Path of Exile filter generation and economy data analysis.',
    'long_description': None,
    'author': 'David Gidwani',
    'author_email': 'david.gidwani@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
