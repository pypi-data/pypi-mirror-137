# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ptijson']

package_data = \
{'': ['*']}

install_requires = \
['argcomplete>=2.0.0,<3.0.0',
 'jmespath>=0.10.0,<0.11.0',
 'prompt-toolkit>=3.0.26,<4.0.0']

entry_points = \
{'console_scripts': ['ijson = ptijson:_main', 'ptijson = ptijson:_main']}

setup_kwargs = {
    'name': 'ptijson',
    'version': '0.1.0',
    'description': 'Interactive JSON queries, built on prompt toolkit and jmespath',
    'long_description': '# Interactive JSON queries, built on prompt toolkit and jmespath\n![Example](./demo.gif)\n\n## Installation\nRecommended installation is with [pipx](https://github.com/pypa/pipx):\n```bash\npython3 -m pip install --user pipx\npython3 -m pipx ensurepath\npython3 -m pipx install ptijson\n```\n',
    'author': 'Aatif Syed',
    'author_email': 'aatifsyedyp@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aatifsyed/ptijson',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
