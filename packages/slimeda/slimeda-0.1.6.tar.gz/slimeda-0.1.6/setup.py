# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['slimeda']

package_data = \
{'': ['*']}

install_requires = \
['altair>=4.2.0,<5.0.0', 'numpy>=1.22.1,<2.0.0', 'pandas>=1.3.5,<2.0.0']

setup_kwargs = {
    'name': 'slimeda',
    'version': '0.1.6',
    'description': 'Slim version of EDA processing Python package',
    'long_description': '# slimeda\n[![ci-cd](https://github.com/UBC-MDS/slimeda/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/UBC-MDS/slimeda/actions/workflows/ci-cd.yml)\n\n\nExploratory Data Analysis is an important preparatory work to help data scientists understand and clean up data sets before machine learning begins. However, this step also involves a lot of repetitive tasks. In this context, slimeda will help data scientists quickly complete the initial work of EDA and gain a preliminary understanding of the data.\n\nSlimeda focuses on unique value and missing value counts, as well as making graphs like histogram and correlation graphs. Also, the generated results are designed as charts or images, which will help users more flexibly reference their EDA results.\n\n## Function Specification\n\nThe package is under developement and includes the following functions:\n\n- **histogram** : This function accepts a dataframe and builds histograms for all numeric columns which are returned \nas an array of chart objects.\n\n- **corr_map** : This function accepts a dataframe and builds an heat map for all numeric columns which is returned \nas a chart object.\n\n- **cat_unique_count** : This function accepts a dataframe and returns a table of unique value counts for all categorical columns.\n\n- **miss_counts** : This function accepts a dataframe and returns a table of counts of missing values in all columns.\n\nLimitations:\nWe only consider numeric and categorical columns in our package.\n\n## Installation\n\n```bash\n$ pip install git+https://github.com/UBC-MDS/slimeda\n```\n## Usage\n\nSlimeda has **FOUR** functions to help you conduct basic EDA(Exploratory Data Analysis), which includes four basic functions:\n\n- **histogram** : \nThe histogram function accepts a data frame as input and a list of columns, and returns a list of charts. Each chart in the output is a histogram Altair object (mark_bar) with the given column on the x-axis and the the count on the y-axis.\n    - histogram(example_1, ["Age", "Hobby"])\n    - **OUTPUT**:\n    an Altair histogram object\n\n- **corr_map** : Plot the correlation maps based on the provided dataframe and its columns. It will plot the (pairwise) correlation map using the [Spearman\'s rand correlation coefficient](https://en.wikipedia.org/wiki/Spearman%27s_rank_correlation_coefficient).\n    - Required parameters in this function:\n        - df: a pd.dataframe containing the data of interest\n        - columns: the columns of interest\n            - Notice that only numeric columns will be included in the final map  \n    - `from vega_datasets import data`\n    - `corr_map(data.cars(), data.cars().columns.to_list())`\n\n![Output of corr_map](https://i.ibb.co/vcrZd17/visualization.png)\n\n- **cat_unique_counts** : Returns the unique count of values in a categorical features and the corresponding feature name.\n    - Required parameters in this function:\n        - df: a pd.dataframe you want to analyze\n    - `cat_unique_counts(df)`\n\n- **miss_counts** : Return the missing value counts and corresponding percentage for a pd.dataframe.\n    - There are four parameters in this function:\n        - df: a pd.dataframe you want to analyze\n        - keyword: Default is None, a single number or string that you want to define as NaN along with original NaNs\n        - sparse: a boolean value defaulted as False, meaning don\'t show columns without null values False\n        - ascending: a boolean value defaulted as False, help you to sort the counts ascending or decending.\n    - `miss_counts(example_1,keyword="miss",sparse=False,ascending=False)`\n    - **OUTPUT**:\n        - a pd.dataframe as below:\n    \n![The output of miss_counts](https://i.ibb.co/1LpM9mZ/20220127141909.png)\n\n## Documentation\n\nPlease see the documentation for this package on the Read the Docs [link](https://slimeda.readthedocs.io/en/latest/index.html)\n\n## Fitting in Python Ecosystem\n- Packages have similar functions are:\n    -  [numpy](https://numpy.org/): can count unique value and missing value\n    - [pandas-profiling](https://pandas-profiling.github.io/pandas-profiling/docs/master/rtd/): can generate basic eda reports.\n- Slimeda\'s innovation points:\n\n    - We aggregate necessary functions for eda in one function that can only be done with multiple packages and simplify the code. For example, for missing value counts, we not only get the counts but also calculate its percentage.\n    - Compared with numpy, we optimize the output to be more clear.\n    - Compared with pandas-profiling, we generate the most commonly used graphs and make possible for png outputs, which is much more flexible for users to get their eda results.\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## CONTRIBUTORS\n\nGroup 4 members:\n- Khalid Abdilahi (@khalidcawl)\n- Anthea Chen (@anthea98)\n- Simon Guo (@y248guo)\n- Taiwo Owoseni (@thayeylolu)\n\n\n## License\n\n`slimeda` was created by Simon Guo. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`slimeda` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Simon Guo',
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
