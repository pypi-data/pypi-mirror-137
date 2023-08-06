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
    'version': '0.1.1',
    'description': '',
    'long_description': '# echo1-coco-split\necho1-coco-split provides a faster, safer way to split coco formatted datasets into train, validation and test sets. \n\n## Installation & Use\n```shell\n# Install echo1-coco-split\npip install echo1-coco-split\n\n# Run the coco-split\ncoco-split \\\n    --has_annotations \\\n    --valid_ratio .2 \\\n    --test_ratio .1 \\\n    --annotations_file ./annotations/instances_default.json\n```\n\n## coco-split help\n```shell\nusage: coco-split [-h] --annotations_file ANNOTATIONS_FILE --valid_ratio VALID_RATIO --test_ratio\n                  TEST_RATIO [--train_name TRAIN_NAME] [--valid_name VALID_NAME] [--test_name TEST_NAME]\n                  [--has_annotations]\ncoco-split: error: the following arguments are required: --annotations_file, --valid_ratio, --test_ratio\n```\n',
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
