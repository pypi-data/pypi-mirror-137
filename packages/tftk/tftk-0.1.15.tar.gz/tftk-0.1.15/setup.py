# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tftk',
 'tftk.augment_ok',
 'tftk.dataset',
 'tftk.image',
 'tftk.image.dataset',
 'tftk.image.model',
 'tftk.loss',
 'tftk.optimizer',
 'tftk.optuna',
 'tftk.patch',
 'tftk.rl',
 'tftk.train']

package_data = \
{'': ['*']}

install_requires = \
['graphviz>=0.14',
 'icrawler>=0.6.2',
 'matplotlib>=3.2.1,<4.0.0',
 'optuna>=1.2',
 'pillow>=7.0.0',
 'pybullet>=2.8.2,<3.0.0',
 'pydot-ng>=2.0.0',
 'pymongo>=3.10.1,<4.0.0',
 'pyspark>=3.2.0,<4.0.0',
 'scikit-learn>=1.0.1,<2.0.0',
 'sphinx>=3.0.3,<4.0.0',
 'sphinx_materialdesign_theme>=0.1.11,<0.2.0',
 'sphinx_ustack_theme>=1.0.0,<2.0.0',
 'tensorboard_plugin_profile>=2.2.0',
 'tensorflow-datasets>=4,<5',
 'tensorflow>=2.2',
 'tensorflow_addons>=0.12.1',
 'tensorflow_metadata>=0.27.0']

setup_kwargs = {
    'name': 'tftk',
    'version': '0.1.15',
    'description': 'Machine Learning Toolkit using TensorFlow',
    'long_description': None,
    'author': 'Naruhide KITADA',
    'author_email': 'kitfactory@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
