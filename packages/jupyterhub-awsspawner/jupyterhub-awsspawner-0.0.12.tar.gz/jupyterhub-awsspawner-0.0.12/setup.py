# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['awsspawner']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.20.46,<2.0.0', 'jupyterhub>=1.4.1']

setup_kwargs = {
    'name': 'jupyterhub-awsspawner',
    'version': '0.0.12',
    'description': 'Spawns JupyterHub single user servers in Docker containers running in AWS ECS Task (include EC2、Fargate、Fargate Spot)',
    'long_description': '# awsspawner\nSpawns JupyterHub single user servers in Docker containers running in AWS ECS Task (include EC2、Fargate、Fargate Spot)\n',
    'author': 'kackyt',
    'author_email': 't_kaki@nextappli.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/adacotech/awsspawner',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
