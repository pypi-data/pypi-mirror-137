# snapedautility

[![ci-cd](https://github.com/UBC-MDS/snapedautility/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/UBC-MDS/snapedautility/actions/workflows/ci-cd.yml) [![Documentation Status](https://readthedocs.org/projects/snapedautility/badge/?version=latest)]

[![codecov](https://codecov.io/gh/UBC-MDS/snapedautility/branch/master/graph/badge.svg?token=JQMCLklaav)](https://codecov.io/gh/UBC-MDS/snapedautility)

snapedautility is an open-source library that generate useful function to kickstart EDA (Exploratory Data Analysis) with just a few lines of code. The system is built around quickly **analyzing the whole dataset** and **providing a detailed report with visualization**. Its goal is to help quick analysis of feature characteristics, detecting outliers from the observations and other such data characterization tasks.
## Features
1. `plot_histograms`: Plots the distribution for numerical, categorical and text features
2. `detect_outliers`: Generate a violin plot that indicates the outliers that deviate from other observations on data.
3. `plot_corr`: Generates Correlation Plots for numerical (Pearson's correlation), categorical (uncertainty coefficient) and categorical-numerical (correlation ratio) datatypes seamlessly for all data types.
## Installation

```bash
$ pip install snapedautility
```

## Usage

### plot_histograms
```
>>> from snapedautility.plot_histograms import plot_histograms
>>> df = penguins_data
>>> plot_histograms(df, ["Culmen Length (mm)", "Culmen Depth (mm)", 'Species'], 100, 100)
```

### plot_corr
```
>>> from snapedautility.plot_corr import plot_corr
>>> df = penguins_data
>>> plot_corr(df, ["Culmen Length (mm)", "Culmen Depth (mm)", 'Species'])
```

### detect_outliers
```
>>> from snapedautility.detect_outliers import detect_outliers 
>>> s = pd.Series([1,1,2,3,4,5,6,9,10,13,40])
>>> detect_outliers(s)
```

## Documentation

The official documentation is hosted on Read the Docs: https://snapedautility.readthedocs.io/

## Contributors

|  	 Core contributor| Github.com username| 
|---------|---|
|  Kyle Ahn |  @AraiYuno | 
|  Harry Chan |  @harryyikhchan | 
|  Dongxiao Li | @dol23asuka | 

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## Similar Work

We recognize EDA (exploratory data analysis) and preprocessing packages are common in the Python open source ecosystem. Our package aims to do a few things very well, and be light weight. A non exhaustive list of EDA helper packages in Python include:

- [`pandasprofiling`](https://github.com/pandas-profiling/pandas-profiling)
    - This was the original inspiration for this project. We would like to expand the functionalities on this project.
- [`sweetviz`](https://github.com/fbdesignpro/sweetviz)
    - This package produces very clean visuals detailing breakdowns in descriptive statistics and can do so with train/test sets for model building workflows.
- [`ExploriPy`](https://github.com/exploripy/exploripy)
    - This packages does the most common EDA tasks but also adds in the ability to do statistical testing using analysis of variance (ANOVA), Chi Square test of independence etc.

## License

`snapedautility` was created by Kyle Ahn, Harry Chan and Dongxiao Li. It is licensed under the terms of the MIT license.

## Credits

`snapedautility` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
