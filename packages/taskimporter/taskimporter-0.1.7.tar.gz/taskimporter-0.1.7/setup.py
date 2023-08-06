# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['taskimporter', 'taskimporter.services', 'taskimporter.task_managers']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.0.3,<4.0.0',
 'PyGithub>=1.55,<2.0',
 'appdirs>=1.4.4,<2.0.0',
 'jira>=3.1.1,<4.0.0',
 'python-gitlab>=2.10.1,<3.0.0']

entry_points = \
{'console_scripts': ['taskimporter = taskimporter:main']}

setup_kwargs = {
    'name': 'taskimporter',
    'version': '0.1.7',
    'description': 'Tool to import tasks from a variety of sources into a task manager',
    'long_description': None,
    'author': 'Joshua Mulliken',
    'author_email': 'joshua@mulliken.net',
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
