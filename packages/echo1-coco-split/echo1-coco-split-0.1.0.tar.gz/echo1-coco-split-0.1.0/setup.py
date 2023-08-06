# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['echo1_coco_split']

package_data = \
{'': ['*']}

install_requires = \
['funcy>=1.17,<2.0', 'scikit-learn>=1.0.2,<2.0.0']

entry_points = \
{'console_scripts': ['coco-split = echo1_coco_split.echo1_coco_split:main']}

setup_kwargs = {
    'name': 'echo1-coco-split',
    'version': '0.1.0',
    'description': '',
    'long_description': '# echo1-coco-split\necho1-coco-split provides a faster, safer way to split coco formatted datasets into train, validation and test sets.\n\n```shell\npython echo1_coco_split.py --has_annotations --valid_ratio .2 --test_ratio .1 --annotations_file /Users/michael/Downloads/export_all/annotations/instances_default.json\n```',
    'author': 'Michael Mohamed',
    'author_email': 'michael.mohamed@echo1.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/e1-io/echo1-coco-builder',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
