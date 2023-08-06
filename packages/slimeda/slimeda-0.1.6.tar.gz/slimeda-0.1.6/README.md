# slimeda
[![ci-cd](https://github.com/UBC-MDS/slimeda/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/UBC-MDS/slimeda/actions/workflows/ci-cd.yml)


Exploratory Data Analysis is an important preparatory work to help data scientists understand and clean up data sets before machine learning begins. However, this step also involves a lot of repetitive tasks. In this context, slimeda will help data scientists quickly complete the initial work of EDA and gain a preliminary understanding of the data.

Slimeda focuses on unique value and missing value counts, as well as making graphs like histogram and correlation graphs. Also, the generated results are designed as charts or images, which will help users more flexibly reference their EDA results.

## Function Specification

The package is under developement and includes the following functions:

- **histogram** : This function accepts a dataframe and builds histograms for all numeric columns which are returned 
as an array of chart objects.

- **corr_map** : This function accepts a dataframe and builds an heat map for all numeric columns which is returned 
as a chart object.

- **cat_unique_count** : This function accepts a dataframe and returns a table of unique value counts for all categorical columns.

- **miss_counts** : This function accepts a dataframe and returns a table of counts of missing values in all columns.

Limitations:
We only consider numeric and categorical columns in our package.

## Installation

```bash
$ pip install git+https://github.com/UBC-MDS/slimeda
```
## Usage

Slimeda has **FOUR** functions to help you conduct basic EDA(Exploratory Data Analysis), which includes four basic functions:

- **histogram** : 
The histogram function accepts a data frame as input and a list of columns, and returns a list of charts. Each chart in the output is a histogram Altair object (mark_bar) with the given column on the x-axis and the the count on the y-axis.
    - histogram(example_1, ["Age", "Hobby"])
    - **OUTPUT**:
    an Altair histogram object

- **corr_map** : Plot the correlation maps based on the provided dataframe and its columns. It will plot the (pairwise) correlation map using the [Spearman's rand correlation coefficient](https://en.wikipedia.org/wiki/Spearman%27s_rank_correlation_coefficient).
    - Required parameters in this function:
        - df: a pd.dataframe containing the data of interest
        - columns: the columns of interest
            - Notice that only numeric columns will be included in the final map  
    - `from vega_datasets import data`
    - `corr_map(data.cars(), data.cars().columns.to_list())`

![Output of corr_map](https://i.ibb.co/vcrZd17/visualization.png)

- **cat_unique_counts** : Returns the unique count of values in a categorical features and the corresponding feature name.
    - Required parameters in this function:
        - df: a pd.dataframe you want to analyze
    - `cat_unique_counts(df)`

- **miss_counts** : Return the missing value counts and corresponding percentage for a pd.dataframe.
    - There are four parameters in this function:
        - df: a pd.dataframe you want to analyze
        - keyword: Default is None, a single number or string that you want to define as NaN along with original NaNs
        - sparse: a boolean value defaulted as False, meaning don't show columns without null values False
        - ascending: a boolean value defaulted as False, help you to sort the counts ascending or decending.
    - `miss_counts(example_1,keyword="miss",sparse=False,ascending=False)`
    - **OUTPUT**:
        - a pd.dataframe as below:
    
![The output of miss_counts](https://i.ibb.co/1LpM9mZ/20220127141909.png)

## Documentation

Please see the documentation for this package on the Read the Docs [link](https://slimeda.readthedocs.io/en/latest/index.html)

## Fitting in Python Ecosystem
- Packages have similar functions are:
    -  [numpy](https://numpy.org/): can count unique value and missing value
    - [pandas-profiling](https://pandas-profiling.github.io/pandas-profiling/docs/master/rtd/): can generate basic eda reports.
- Slimeda's innovation points:

    - We aggregate necessary functions for eda in one function that can only be done with multiple packages and simplify the code. For example, for missing value counts, we not only get the counts but also calculate its percentage.
    - Compared with numpy, we optimize the output to be more clear.
    - Compared with pandas-profiling, we generate the most commonly used graphs and make possible for png outputs, which is much more flexible for users to get their eda results.
## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## CONTRIBUTORS

Group 4 members:
- Khalid Abdilahi (@khalidcawl)
- Anthea Chen (@anthea98)
- Simon Guo (@y248guo)
- Taiwo Owoseni (@thayeylolu)


## License

`slimeda` was created by Simon Guo. It is licensed under the terms of the MIT license.

## Credits

`slimeda` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
