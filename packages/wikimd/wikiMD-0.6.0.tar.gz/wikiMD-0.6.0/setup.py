# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['wikiMD']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.0.3,<4.0.0', 'wikipedia>=1.4.0,<2.0.0']

entry_points = \
{'console_scripts': ['wikimd = wikiMD.script:run']}

setup_kwargs = {
    'name': 'wikimd',
    'version': '0.6.0',
    'description': 'Turn Wikipedia in markmap friendly markdown',
    'long_description': None,
    'author': 'John Capobianco',
    'author_email': 'ptcapo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
