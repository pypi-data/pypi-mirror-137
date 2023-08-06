# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src', 'src.beam_sequencer']

package_data = \
{'': ['*']}

install_requires = \
['apache-beam[test,gcp]>=2.35.0,<3.0.0', 'pytest==4.4.0']

setup_kwargs = {
    'name': 'pdprecommender',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Yi FU',
    'author_email': 'yi.fu@hm.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
