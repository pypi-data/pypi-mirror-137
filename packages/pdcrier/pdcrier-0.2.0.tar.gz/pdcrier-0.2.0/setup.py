# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pdcrier', 'pdcrier.cli']

package_data = \
{'': ['*']}

install_requires = \
['pdpyras>=4.4.0,<5.0.0', 'pyaml>=21.10.1,<22.0.0']

entry_points = \
{'console_scripts': ['pd-alert = pdcrier.cli.alerts:alerter']}

setup_kwargs = {
    'name': 'pdcrier',
    'version': '0.2.0',
    'description': 'Wrapper scripts for creating PagerDuty alerts',
    'long_description': '# pdcrier\n\nCreate PagerDuty alerts from the command-line.\n\n## Dependencies\n\n- `pdpyras`\n- `pyyaml`',
    'author': 'Joe Block',
    'author_email': 'jpb@unixorn.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/unixorn/pdcrier',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
