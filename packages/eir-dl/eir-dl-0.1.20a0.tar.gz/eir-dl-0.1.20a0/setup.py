# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['eir',
 'eir.data_load',
 'eir.experiment_io',
 'eir.interpretation',
 'eir.models',
 'eir.models.fusion',
 'eir.models.image',
 'eir.models.omics',
 'eir.models.sequence',
 'eir.models.tabular',
 'eir.setup',
 'eir.setup.presets',
 'eir.train_utils',
 'eir.visualization']

package_data = \
{'': ['*']}

install_requires = \
['ConfigArgParse>=1.2.3,<2.0.0',
 'adabelief-pytorch>=0.2.0,<0.3.0',
 'aislib>=0.1.7-alpha.0,<0.2.0',
 'colorama>=0.4.4,<0.5.0',
 'dill>=0.3.3,<0.4.0',
 'hypothesis>=6.14.0,<7.0.0',
 'ipython>=7.28.0,<8.0.0',
 'joblib>=1.1.0,<2.0.0',
 'matplotlib==3.4.3',
 'numpy>=1.19.2,<2.0.0',
 'pandas>=1.2.0,<2.0.0',
 'perceiver-pytorch>=0.8.1,<0.9.0',
 'plotly>=5.3.1,<6.0.0',
 'py>=1.9.0,<2.0.0',
 'pytorch-ignite>=0.4.7,<0.5.0',
 'scikit-learn>=1.0,<2.0',
 'seaborn>=0.11.1,<0.12.0',
 'sentencepiece>=0.1.96,<0.2.0',
 'shap>=0.40.0,<0.41.0',
 'sympy>=1.6.2,<2.0.0',
 'tensorboard>=2.3.0,<3.0.0',
 'timm>=0.5.4,<0.6.0',
 'torch-optimizer>=0.3.0,<0.4.0',
 'torch>=1.10.0,<2.0.0',
 'torchtext>=0.11.0,<0.12.0',
 'torchvision>=0.11.1,<0.12.0',
 'tqdm>=4.55.0,<5.0.0',
 'transformers>=4.11.3,<5.0.0']

entry_points = \
{'console_scripts': ['eirpredict = eir.predict:main',
                     'eirtrain = eir.train:main']}

setup_kwargs = {
    'name': 'eir-dl',
    'version': '0.1.20a0',
    'description': '',
    'long_description': None,
    'author': 'Arnor Sigurdsson',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
