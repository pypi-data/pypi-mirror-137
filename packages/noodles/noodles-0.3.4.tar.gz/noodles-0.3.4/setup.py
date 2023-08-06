# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['noodles',
 'noodles.display',
 'noodles.display.curses',
 'noodles.draw_workflow',
 'noodles.interface',
 'noodles.lib',
 'noodles.patterns',
 'noodles.prov',
 'noodles.run',
 'noodles.run.remote',
 'noodles.run.single',
 'noodles.run.threading',
 'noodles.run.xenon',
 'noodles.serial',
 'noodles.workflow']

package_data = \
{'': ['*']}

install_requires = \
['filelock>=3.4.2,<4.0.0',
 'graphviz>=0.19.1,<0.20.0',
 'h5py>=3.6.0,<4.0.0',
 'numpy>=1.22.2,<2.0.0',
 'pyxenon>=3.0.3,<4.0.0']

setup_kwargs = {
    'name': 'noodles',
    'version': '0.3.4',
    'description': 'Worflow Engine',
    'long_description': None,
    'author': 'Johan Hidding',
    'author_email': 'j.hidding@esciencecenter.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
