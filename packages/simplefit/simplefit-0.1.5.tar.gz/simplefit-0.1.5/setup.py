# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['simplefit']

package_data = \
{'': ['*']}

install_requires = \
['altair-data-server>=0.4.1,<0.5.0',
 'altair-saver>=0.5.0,<0.6.0',
 'altair>=4.2.0,<5.0.0',
 'notebook>=6.4.7,<7.0.0',
 'pandas>=1.3.5,<2.0.0',
 'python-semantic-release>=7.24.0,<8.0.0',
 'sklearn>=0.0,<0.1',
 'vega-datasets>=0.9.0,<0.10.0',
 'vega==1.3.0']

setup_kwargs = {
    'name': 'simplefit',
    'version': '0.1.5',
    'description': 'Package that will clean the data, do basic EDA and provide an insight to basic models, LR and ridge',
    'long_description': "# simplefit\n\n[![ci-cd](https://github.com/UBC-MDS/simplefit/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/UBC-MDS/simplefit/actions/workflows/ci-cd.yml)  [![Documentation Status](https://readthedocs.org/projects/simplefit/badge/?version=latest)](https://simplefit.readthedocs.io/en/latest/?badge=latest) [![codecov](https://codecov.io/gh/UBC-MDS/simplefit/branch/main/graph/badge.svg?token=uMTErqAsGr)](https://codecov.io/gh/UBC-MDS/simplefit)\n\n\nA python package that cleans the data, does basic EDA and returns scores for basic classification and regression models\n<br>\n\n### Overview\nThis package helps data scientists to clean the data, perform basic EDA, visualize graphical interpretations and analyse performance of the baseline model and basic Classification or Regression models, namely Logistic Regression, Ridge on their data.\n\n\n### Functions\n---\n| Function Name | Input                                                                                      | Output                        | Description                                                                                                                          |\n|---------------|--------------------------------------------------------------------------------------------|-------------------------------|--------------------------------------------------------------------------------------------------------------------------------------|\n| cleaner       | `dataframe`                                                                                | list of 3 dataframes          | Loads and cleans the dataset, removes NA rows, strip extra white spaces, etc  and returns clean dataframe                                                    |\n| plot_distributions       | `dataframe`, `bins`, `dist_cols`, `class_label`              | Altair histogram plot object  | creates numerical distribution plots on either all the numeric columns or the ones provided to it  |\n| plot_corr       | `dataframe`, `corr`              | Altair correlation plot object  | creates correlation plot for all the columns in the dataframe |\n| plot_splom       | `dataframe`, `pair_cols`              | Altair SPLOM plot object  | creates SPLOM plot for all the numeric columns in the dataframe or the ones passed by the user |\n| regressor     | `train_df`, `target_col`, `numeric_feats`, `categorical_feats`, `text_col`, `cv`           | `dataframe`                   | Preprocesses the data, fits baseline model(`Dummy Regressor`) and `Ridge` with default setup and returns model scores in the form of a dataframe               |\n| classifier    | `train_df` ,  `target_col` ,  `numeric_feats` ,  `categorical_feats` ,  `text_col` ,  `cv` | `dataframe`                   | Preprocesses the data, fits baseline model(`Dummy Classifier`) and `Logistic Regression` with default setup and returns model scores in the form of a dataframe|\n\n\n\n### Our Package in the Python Ecosystem\n---\nThere exists a subset of our package as standalone packages, namely [auto-eda](https://pypi.org/project/auto-eda/), [eda-report](https://pypi.org/project/eda-report/), [quick-eda](https://pypi.org/project/quick-eda/), [s11-classifier](https://pypi.org/project/s11-classifier/). But these packages only do the EDA or just the classification using `XGBoostClassifier`. But with our package, we aim to do all the basic steps of a ML pipeline and save the data scientist's time and effort by cleaning, preprocessing, returning grpahical visualisations from EDA and providing an insight about the basic model performances, after which the user can decide which other models to use.\n\n\n## Installation\n\n```bash\n$ pip install git+https://github.com/UBC-MDS/simplefit\n```\n\n## Usage\n\n[![Documentation Status](https://readthedocs.org/projects/simplefit/badge/?version=latest)](https://simplefit.readthedocs.io/en/latest/?badge=latest)\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## Contributors\n\nThis python package was developed by the following Master of Data Science program candidates at the University of the British Columbia:\n\n- Mohammadreza Mirzazadeh [@rezam747](https://github.com/rezam747)\n- Zihan Zhou              [@zzhzoe](https://github.com/zzhzoe)\n- Navya Dahiya            [@nd265](https://github.com/nd265)\n- Sanchit Singh           [@Sanchit120496](https://github.com/Sanchit120496)\n\n## License\n\n`simplefit` was created by Reza Zoe Navya Sanchit. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`simplefit` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n",
    'author': 'Reza Zoe Navya Sanchit',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
