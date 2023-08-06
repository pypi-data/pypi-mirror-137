# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['amaz3dpy', 'amaz3dpy.clients', 'amaz3dpy.webapiclients']

package_data = \
{'': ['*']}

install_requires = \
['InquirerPy==0.3.2',
 'appdirs==1.4.4',
 'click==8.0.3',
 'clint==0.5.1',
 'columnar==1.4.1',
 'gql[all]>=3.0.0',
 'pydantic==1.9.0',
 'pyfiglet==0.7.2',
 'pyjwt[crypto]==2.3.0',
 'python-dateutil==2.8.2',
 'timeago==1.0.15']

entry_points = \
{'console_scripts': ['amaz3d = amaz3dpy:amaz3d']}

setup_kwargs = {
    'name': 'amaz3dpy',
    'version': '0.1.3',
    'description': 'Python SDK for AMAZ3D - Powered By Adapta Studio',
    'long_description': '================\nAMAZ3DPY\n================\n\nIntroduction\n============\namaz3dpy is a simple Python SDK to interact with Amaz3d Web APIs.\n\nThe following README will be improved at later time.\n\nCli\n===\nIt is possible to run a simple interactive CLI application for creating projects and optimizations.\nOpen your terminal and run:\n\n    amaz3d\n    ',
    'author': 'Adapta Studio',
    'author_email': 'support@adapta.studio',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9.1,<4.0.0',
}


setup(**setup_kwargs)
