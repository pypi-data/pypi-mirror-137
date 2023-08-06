# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ftt',
 'ftt.cli',
 'ftt.cli.commands',
 'ftt.cli.handlers',
 'ftt.cli.handlers.steps',
 'ftt.cli.renderers',
 'ftt.cli.renderers.portfolio_versions',
 'ftt.cli.renderers.portfolios',
 'ftt.cli.renderers.securities',
 'ftt.cli.renderers.weights',
 'ftt.handlers',
 'ftt.handlers.handler',
 'ftt.handlers.portfolio_steps',
 'ftt.handlers.portfolio_version_steps',
 'ftt.handlers.securities_steps',
 'ftt.handlers.security_prices_steps',
 'ftt.handlers.weights_steps',
 'ftt.portfolio_management',
 'ftt.storage',
 'ftt.storage.data_objects',
 'ftt.storage.mappers',
 'ftt.storage.models',
 'ftt.storage.repositories']

package_data = \
{'': ['*'], 'ftt': ['config/*']}

install_requires = \
['Riskfolio-Lib>=2.0.0,<3.0.0',
 'SQLAlchemy>=1.4.31,<2.0.0',
 'Yahoo-ticker-downloader>=3.0.1,<4.0.0',
 'cvxopt==1.2.7',
 'pandas>=1.4.0,<2.0.0',
 'pandas_datareader>=0.9,<0.10',
 'peewee>=3.14.0,<4.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'pyportfolioopt>=1.2.7,<2.0.0',
 'python-nubia>=0.2b5,<0.3',
 'pyyaml>=6.0,<7.0',
 'result>=0.7.0,<0.8.0',
 'rich>=11.1,<12.0',
 'yfinance>=0.1.54,<0.2.0']

entry_points = \
{'console_scripts': ['ftt = ftt:__main__']}

setup_kwargs = {
    'name': 'ftt',
    'version': '0.1.0',
    'description': 'Financial Trading Tool (FTT) – is an asset management application that helps to make the right decision on time.',
    'long_description': '# FTT\n\n## Financial Trading Tools\n\n> Finance is hard. Programming is hard.\n\nFTT is a financial asset management application that helps to make right decision on time. \n\n## Main features\n\n* Portfolio Building\n* Assets Recommendation\n* Portfolio testing\n* Strategy testing\n* Portfolio value tracking over the time\n* Integration with Interactive Brokers\n* Realtime signals trading decisions\n* Web interface\n* CLI interface\n\n## Collaborators\n- [Artem M](https://github.com/ignar)\n- [Ihor M](https://github.com/IhorMok)\n\n\n## Quickstart\n\n```\npip install ftt\nftt bootstrap\nftt example\n```\n\n\n### Portfolio creation\n\n*Import portfolio configuration from file*\n\n```yaml\nname: S&P companies\nbudget: 10000\nsymbols:\n  - AAPL\n  - MSFT\n  - SHOP\nperiod_start: 2020-01-01\nperiod_end: 2021-01-01\ninterval: 5m\n```\n\n```\nfft> portfolio import sp_companies.yml\n```\n\n*Create weights for portfolio*\n\n```\nftt> portfolio build <ID>\n```\n\n## Development\n\nDependencies\n\n* pyenv\n* poetry\n\n```commandline\npyenv install PYTHON_VERSION\npip install cmake\npoetry update\n```',
    'author': 'Artem Melnykov',
    'author_email': 'melnykov.artem.v@gmail.com',
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
