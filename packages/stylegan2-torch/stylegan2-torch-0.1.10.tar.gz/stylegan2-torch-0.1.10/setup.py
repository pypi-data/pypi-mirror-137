# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stylegan2_torch',
 'stylegan2_torch.discriminator',
 'stylegan2_torch.generator',
 'stylegan2_torch.op']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'stylegan2-torch',
    'version': '0.1.10',
    'description': 'A simple, typed, commented Pytorch implementation of StyleGAN2.',
    'long_description': None,
    'author': 'Peter Yuen',
    'author_email': 'ppeetteerrsx@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
