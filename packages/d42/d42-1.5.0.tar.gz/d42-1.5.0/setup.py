# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['d42']

package_data = \
{'': ['*']}

install_requires = \
['blahblah>=1.5,<1.6',
 'district42>=1.5,<1.6',
 'revolt>=1.5,<1.6',
 'valera>=1.5,<1.6']

setup_kwargs = {
    'name': 'd42',
    'version': '1.5.0',
    'description': 'One package for district42 ecosystem',
    'long_description': '# d42\n\n[![PyPI](https://img.shields.io/pypi/v/d42.svg?style=flat-square)](https://pypi.python.org/pypi/d42/)\n[![PyPI - Downloads](https://img.shields.io/pypi/dm/d42?style=flat-square)](https://pypi.python.org/pypi/d42/)\n[![Python Version](https://img.shields.io/pypi/pyversions/d42.svg?style=flat-square)](https://pypi.python.org/pypi/d42/)\n\nOne package for [district42 ecosystem](https://github.com/topics/district42)\n\nd42 = [district42](https://pypi.org/project/district42/) + [blahblah](https://pypi.org/project/blahblah/) + [valera](https://pypi.org/project/valera/) + [revolt](https://pypi.org/project/revolt/)\n\n## Installation\n\n```sh\npip3 install d42\n```\n\n## Usage\n\n```python\nfrom d42 import schema, fake, validate_or_fail\n\nsch = schema.str("banana")\n\nassert validate_or_fail(sch, fake(sch))\n```\n',
    'author': 'Nikita Tsvetkov',
    'author_email': 'nikitanovosibirsk@yandex.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nikitanovosibirsk/d42',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
