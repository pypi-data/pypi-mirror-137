# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['strangeworks',
 'strangeworks.qiskit',
 'strangeworks.qiskit.backends',
 'strangeworks.qiskit.jobs']

package_data = \
{'': ['*']}

install_requires = \
['qiskit-aer==0.9.1',
 'qiskit-aqua==0.9.5',
 'qiskit-ibmq-provider==0.18.0',
 'qiskit-ignis==0.6.0',
 'qiskit-nature==0.2.1',
 'qiskit-optimization>=0.2.3,<0.3.0',
 'qiskit-terra==0.18.3',
 'qiskit==0.32.0',
 'seaborn==0.11.2',
 'strangeworks>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'strangeworks-qiskit',
    'version': '0.2.2',
    'description': 'Strangeworks extensions',
    'long_description': '| ⚠️    | This SDK is currently in pre-release alpha state and subject to change. To get more info or access to test features check out the [Strangeworks Backstage Pass Program](https://strangeworks.com/backstage). |\n|---------------|:------------------------|\n# Strangeworks Qiskit Extension\n\n Strangeworks Python SDK extension for Qiskit. \n\n\n \n For more information on using the SDK check out the [Strangeworks documentation](https://docs.strangeworks.com/).\n',
    'author': 'Strange Devs',
    'author_email': 'stranger@strangeworks.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
