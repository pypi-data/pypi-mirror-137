# StrapvizPy

![example workflow](https://github.com/UBC-MDS/strapvizpy/actions/workflows/ci-cd.yml/badge.svg)
[![codecov](https://codecov.io/gh/UBC-MDS/strapvizpy/branch/main/graph/badge.svg?token=ufgX4eYuYU)](https://codecov.io/gh/UBC-MDS/strapvizpy)
[![Documentation Status](https://readthedocs.org/projects/strapvizpy/badge/?version=latest)](https://strapvizpy.readthedocs.io/en/latest/?badge=latest)

## Summary

Performs bootstrapping of a sample to produce plots and statistics for use in final reports and documents.

The purpose of this package is to simplify and automate the process of creating simple bootstrap distributions of numerical samples. The package has a module which intakes a sample and relevant parameters such as the desired confidence bounds and number of simulations. The module will perform the simulation statistics to generate the bootstrap distribution and relevant statistics such as the sample mean and bootstrapped confidence interval. The package also has a module for visualization of the bootstraped confidence interval, and for creating a professional publication-ready table of the relevant statistics.

## Package context within the Python ecosystem

The package builds on NumPy and Matplotlib packages, and is designed to conduct bootstrap sampling and visualization using them. scikit-learn has a utils module with a [resample](https://scikit-learn.org/stable/modules/generated/sklearn.utils.resample.html) method which has bootstrapping functionality. But **StrapvizPy** streamlines the process of bootstrapping from data to visualization and embedding in documents which is not available as a single bundle. Some tutorials on bootstrap confidence intervals from [machinelearningmastery.com](https://machinelearningmastery.com/calculate-bootstrap-confidence-intervals-machine-learning-results-python/) and [towardsdatascience.com](https://towardsdatascience.com/bootstrapping-using-python-and-r-b112bb4a969e) encourage the reader to plot the results manually.


## Installation

```bash
$ pip install strapvizpy
```

## Usage

To import `strapvizpy` and check the version:

```python
import strapvizpy
print(strapvizpy.__version__)
```

To import the suite of functions:

```python
from strapvizpy import bootstrap
from strapvizpy import display
```

Please view our packaged documentation [here](https://strapvizpy.readthedocs.io/en/latest/).

## Functions

- `bootstrap_distribution`: Returns a sampling distribution of specified replicates is generated for a specified estimator with replacement for a given bootstrap sample size.  
- `calculate_boot_stats`: Calculates a confidence interval for a given sampling distribution as well as other bootstrapped statistics.  
- `plot_ci`: Creates a histogram of a bootstrapped sampling distribution with its confidence interval and observed sample statistic.  
- `tabulate_stats`: Generates a table that contains a given sampling distribution's mean and standard deviation along with relevant statistics as well as a summary table of the bootstrap distributions parameters. The code automatically saves the tables as html documents.

## Contributing
Julien Gordon, Gautham Pughazhendhi, Zack Tang, and Margot Vore.

## License

`StrapvizPy` was created by Julien Gordon, Gautham Pughazhendhi, Zack Tang, Margot Vore. It is licensed under the terms of the MIT license.

## Credits

`StrapvizPy` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
