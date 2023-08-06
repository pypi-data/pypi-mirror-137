# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypelinez']

package_data = \
{'': ['*']}

install_requires = \
['chuy>=1.4.0,<2.0.0',
 'click>=8.0.3,<9.0.0',
 'colorama>=0.4.4,<0.5.0',
 'semantic-version>=2.8.5,<3.0.0',
 'toml>=0.10.2,<0.11.0',
 'twine>=3.8.0,<4.0.0']

entry_points = \
{'console_scripts': ['pypelinez = pypelinez.main:main']}

setup_kwargs = {
    'name': 'pypelinez',
    'version': '0.6.1',
    'description': '',
    'long_description': '# Pypelines\n\n## Description\nPython command line tool to support CI/CD for various platforms\n\n[![pipeline status](https://gitlab.com/thecb4/pypelinez/badges/main/pipeline.svg)](https://gitlab.com/thecb4/pypelinez/-/commits/main)\n\n-- images --\n\n## Installation\npip install pypelinez\n\n## Usage\n```shell\n$ pypelinez feature start <feature/feature-name>\n```\n\nCurrent commands:\n* feature start\n* feature add-commit\n* feature submit\n* feature finish\n* release start <version>\n* release add-commit\n* release submit\n* release finish\n* release publish-start\n\n## Support\n\n## Roadmap\n[ ] apple version bump\n[ ] android version bump\n[ ] documentation\n[ ] Simplify version bump process\n\n## Contributing\n\n## Authors and Acknowledgements\n\n## License\n[MIT](https://choosealicense.com/licenses/mit/)',
    'author': 'thecb4',
    'author_email': 'cavelle@thecb4.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/thecb4/pypelinez',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
