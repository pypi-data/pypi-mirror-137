# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['botpress_nlu_testing']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0',
 'dynaconf>=3.1.7,<4.0.0',
 'numpy>=1.22.1,<2.0.0',
 'pandas>=1.4.0,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'rich>=11.1.0,<12.0.0',
 'scikit-learn>=1.0.2,<2.0.0',
 'streamlit>=1.5.0,<2.0.0']

entry_points = \
{'console_scripts': ['launch = botpress_nlu_testing.cli:main']}

setup_kwargs = {
    'name': 'botpress-nlu-testing',
    'version': '0.1.0',
    'description': 'A package to test botpress bots and return performance informations.',
    'long_description': 'None',
    'author': 'Pierre Snell',
    'author_email': 'pierre.snell@botpress.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
