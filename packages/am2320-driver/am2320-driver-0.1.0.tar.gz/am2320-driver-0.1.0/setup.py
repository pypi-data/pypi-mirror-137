# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['am2320_driver']

package_data = \
{'': ['*']}

install_requires = \
['smbus2>=0.4.1,<0.5.0']

setup_kwargs = {
    'name': 'am2320-driver',
    'version': '0.1.0',
    'description': 'This is pip package for using AM2320 Digital Temperature and Humidity Sensor.',
    'long_description': '# am2320-driver-py\n\nThis is pip package for using AM2320 Digital Temperature and Humidity Sensor.\n',
    'author': 'chanyou0311',
    'author_email': 'chanyou0311@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/chanyou0311/am2320-driver-py',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
