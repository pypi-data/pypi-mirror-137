# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drawitor']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.0.1,<10.0.0']

entry_points = \
{'console_scripts': ['drawitor = drawitor:main']}

setup_kwargs = {
    'name': 'drawitor',
    'version': '0.1.1',
    'description': 'Draw Images or GIFs in your terminal.',
    'long_description': '## Drawitor\n\nDraw Images/GIFs in your terminal.\n\n## Install\n\n```sh\npip install drawitor\n```\n\n## CLI Tool\n\n```sh\ndrawitor cat_dancing.gif\n```\n\n## Library\n\nThe library is written in a simple functional style.\n\n```python\nfrom drawitor import draw\n\ndraw("my_img.png")\n\ndraw("super_cute_dog.gif")\n```\n\nCheck the CLI tool [source code](./drawitor/__main__.py) for an usage example.\n\n## Licence\n\nReleased under the MIT Licence\n',
    'author': 'Eliaz Bobadilla',
    'author_email': 'eliaz.bobadilladev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/UltiRequiem/drawitor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
