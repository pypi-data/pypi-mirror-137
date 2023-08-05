# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['linefolio', 'linefolio.tests', 'linefolio.tests.test_data']

package_data = \
{'': ['*'], 'linefolio': ['examples/*']}

install_requires = \
['empyrical>=0.5.5,<0.6.0',
 'ipython>=8.0.1,<9.0.0',
 'matplotlib>=3.5.1,<4.0.0',
 'numpy>=1.22.1,<2.0.0',
 'pandas>=1.4.0,<2.0.0',
 'pytz>=2021.3,<2022.0',
 'quantrocket-moonshot>=2.6.0,<3.0.0',
 'scikit-learn>=1.0.2,<2.0.0',
 'scipy>=1.7.3,<2.0.0',
 'seaborn>=0.11.2,<0.12.0']

setup_kwargs = {
    'name': 'linefolio',
    'version': '1.6.0',
    'description': 'Backtest performance analysis and charting for MoonLine, but with pyfolio.',
    'long_description': None,
    'author': 'Tim Wedde',
    'author_email': 'tim.wedde@genzai.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
