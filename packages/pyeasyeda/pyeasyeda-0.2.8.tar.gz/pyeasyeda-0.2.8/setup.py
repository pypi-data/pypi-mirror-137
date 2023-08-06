# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyeasyeda']

package_data = \
{'': ['*']}

install_requires = \
['altair>=4.2.0,<5.0.0',
 'matplotlib>=3.5.1,<4.0.0',
 'numpy>=1.22.1,<2.0.0',
 'pandas>=1.3.5,<2.0.0',
 'seaborn>=0.11.2,<0.12.0']

setup_kwargs = {
    'name': 'pyeasyeda',
    'version': '0.2.8',
    'description': 'Make exploratory data analysis easier! ',
    'long_description': '# pyeasyeda\n\n[![ci-cd](https://github.com/UBC-MDS/pyeasyeda/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/UBC-MDS/pyeasyeda/actions/workflows/ci-cd.yml) [![codecov](https://codecov.io/gh/UBC-MDS/pyeasyeda/branch/main/graph/badge.svg?token=vaOyqFqkor)](https://codecov.io/gh/UBC-MDS/pyeasyeda)\n\nSince exploratory data analysis is an imperative part of every analysis, this package aims at providing efficient data scrubbing and visualization tools to perform preliminary EDA on raw data. The package can be leveraged to clean the dataset and visualize relationships between features to generate insightful trends.\n\n## Functions\n\n-   `clean_up` - This function takes in a pandas dataframe object and performs initial steps of EDA on unstructured data. It returns a clean dataset by removing null values and identifying potential outliers in numeric variables based on a defined threshold.\n\n-   `birds_eye_view` - This function takes in a pandas dataframe object and visualizes the distributions of variables in the form of histograms and density plots. It also generates a correlation heatmap for numeric variables to study their relationships.\n\n-   `close_up` - This function accepts a pandas dataframe object creates a scatterplot of the variable(s) most strongly correlated with the dependent variable. The plot also produces a trend line to model the correlation between the variables.\n\n-   `summary_suggestions` - This function takes in a pandas dataframe object and outputs a table of summary statistics for numeric and categorical variables and a table for percentage of unique values in the categorical variables.\n\nOther packages that offer similar functionality are:\n- [datascience_eda](https://github.com/UBC-MDS/datascience_eda)\n- [QuickDA](https://github.com/sid-the-coder/QuickDA)\n- [easy-data-analysis](https://github.com/jschnab/easy-data-analysis)\n\n## Installation\n\n```bash\n$ pip install pyeasyeda\n```\n\n## Usage\nAfter installing the package through the command above, please run the following commands in the terminal from the root of the project repo as a quick demo. \n```\npython\nimport pandas as pd\nfrom pyeasyeda.clean_up import clean_up\nfrom pyeasyeda.birds_eye_view import birds_eye_view\nfrom pyeasyeda.close_up import close_up\nfrom pyeasyeda.summary_suggestions import summary_suggestions\ndf = pd.read_csv("tests/data/penguins_test.csv")\nclean_up(df)\nplots = birds_eye_view(df)\nclose_up(df, 1)\nsummary_suggestions(df)\n\n```\nPlease check our official documentation for the example usage of the package at [pyeasyeda/example](https://pyeasyeda.readthedocs.io/en/latest/example.html) on Read the Docs.\n\n## Documentation\nThe official documentation is hosted at [pyeasyeda](https://pyeasyeda.readthedocs.io/en/latest/) on Read the Docs.\n\n## Contributors\nThis python package was developed by James Kim, Kristin Bunyan, Luming Yang and Sukhleen Kaur. The team is from the Master of Data Science program at the University of the British Columbia.\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`pyeasyeda` was created by James Kim, Kristin Banyan, Luming Yang and Sukhleen Kaur. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`pyeasyeda` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Luming Yang',
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
