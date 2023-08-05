# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gitops', 'gitops.common', 'gitops.utils']

package_data = \
{'': ['*']}

install_requires = \
['boto3',
 'colorama>=0.4.4,<0.5.0',
 'dsnparse',
 'humanize>=3.5.0,<4.0.0',
 'invoke',
 'pyyaml>=5.1.2',
 'tabulate>=0.8.9,<0.9.0']

extras_require = \
{'server': ['fastapi',
            'httpx>=0.18.1,<0.19.0',
            'uvicorn>=0.13.4,<0.14.0',
            'uvicorn>=0.13.4,<0.14.0',
            'sentry-sdk>=1.3.0,<2.0.0',
            'kubernetes_asyncio>=12.1.2,<13.0.0']}

entry_points = \
{'console_scripts': ['gitops = gitops.main:program.run']}

setup_kwargs = {
    'name': 'gitops',
    'version': '0.8.7',
    'description': 'Manage multiple apps across one or more k8s clusters.',
    'long_description': None,
    'author': 'Jarek Głowacki',
    'author_email': 'jarekwg@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
