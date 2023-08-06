# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mlgw_bns']

package_data = \
{'': ['*'], 'mlgw_bns': ['data/*']}

install_requires = \
['PyCBC>=1.18.3,<2.0.0',
 'h5py>=3.6.0,<4.0.0',
 'joblib>=1.1.0,<2.0.0',
 'numba>=0.55.0,<0.56.0',
 'numpy>=1.18,<1.22',
 'optuna>=2.10.0,<3.0.0',
 'plotly>=5.5.0,<6.0.0',
 'scikit-learn>=1.0.1,<2.0.0',
 'sortedcontainers>=2.4.0,<3.0.0',
 'tqdm>=4.62.3,<5.0.0',
 'types-setuptools>=57.4.7,<58.0.0']

extras_require = \
{'docs': ['Sphinx>=4.3.1,<5.0.0',
          'sphinx-rtd-theme>=1.0.0,<2.0.0',
          'readthedocs-sphinx-search>=0.1.1,<0.2.0',
          'myst-parser>=0.15.2,<0.16.0'],
 'torch': ['torch>=1.10.2,<2.0.0']}

setup_kwargs = {
    'name': 'mlgw-bns',
    'version': '0.6.1',
    'description': 'Accelerating gravitational wave template generation with machine learning.',
    'long_description': "[![CI Pipeline for mlgw_bns](https://github.com/jacopok/mlgw_bns/actions/workflows/ci.yaml/badge.svg)](https://github.com/jacopok/mlgw_bns/actions/workflows/ci.yaml)\n[![Documentation Status](https://readthedocs.org/projects/mlgw-bns/badge/?version=latest)](https://mlgw-bns.readthedocs.io/en/latest/?badge=latest)\n\n# Machine Learning for Gravitational Waves from Binary Neutron Star mergers\n\nThis package's purpose is to speed up the generation of template gravitational waveforms for binary neutron star mergers by training a machine learning model on a dataset of waveforms generated with some physically-motivated surrogate.\n\nIt is able to reconstruct them with mismatches lower than 1/10000,\nwith as little as 1000 training waveforms; \nthe accuracy then steadily drops as more training waveforms are used.\n\nCurrently, the only model used for training is [`TEOBResumS`](http://arxiv.org/abs/1806.01772),\nbut it is planned to introduce the possibility to use others.\n\nThe documentation can be found [here](https://mlgw-bns.readthedocs.io/en/latest).\n\n![dependencygraph](mlgw_bns.svg)\n\n## Installation\n\nTo install the package, use\n```bash\npip install mlgw-bns\n```\n\nFor more details see [the documentation](https://mlgw-bns.readthedocs.io/en/latest/usage_guides/install.html).\n\n## Inner workings\n\nThe main steps taken by `mlgw_bns` to train on a dataset are as follows:\n\n- generate the dataset \n- decompose the Fourier transforms of the waveforms into phase and amplitude\n- downsample the dataset to a few thousand points\n- apply a PCA to reduce the dimensionality to a few tens of real numbers\n- train a neural network on the relation\n    between the waveform parameters and the PCA components\n\nIn several of these steps data-driven optimizations are performed:\n\n- the points at which the waveforms are downsampled are not uniformly chosen:\n    instead, a greedy downsampling algorithm determines them\n- the PCA is trained on a separate downsampled dataset, which is then thrown out\n- the hyperparameters for the neural network are optimized according to both\n    the time taken for the training and the estimated reconstruction error\n\n",
    'author': 'Jacopo Tissino',
    'author_email': 'jacopo@tissino.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jacopok/mlgw_bns',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
