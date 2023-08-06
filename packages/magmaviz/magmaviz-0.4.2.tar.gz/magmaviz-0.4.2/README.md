# magmaviz

[![ci-cd](https://github.com/UBC-MDS/magmaviz/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/UBC-MDS/magmaviz/actions/workflows/ci-cd.yml)
[![codecov](https://codecov.io/gh/UBC-MDS/magmaviz/branch/main/graph/badge.svg?token=x4djzZhNFV)](https://codecov.io/gh/UBC-MDS/magmaviz)
[![Documentation Status](https://readthedocs.org/projects/magmaviz/badge/?version=latest)](https://magmaviz.readthedocs.io/en/latest/?badge=latest)

Exploratory Data Analysis is one of the key steps in a machine learning project. This package aims to make this process easy by providing python functions based on the 'Altair' package to plot four common types of plots with the magma color scheme. To maximize interpretability, the plots have defined color schemes (discrete, diverging, sequential) based on the kind of data they show.

## Installation

```bash
$ pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple magmaviz
```

## Usage 

The interactive version of the usage section can be found here: 

[![Documentation Status](https://readthedocs.org/projects/magmaviz/badge/?version=latest)](https://magmaviz.readthedocs.io/en/latest/?badge=latest)


This package defines four data visualization functions, all with a magma color scheme. They are meant to be used in any data analysis projects using Python. 

### Boxplot

Returns a boxplot based on a data frame, a numerical feature to view the distribution of and a categorical feature to bucket data into categories. Additionally, there is a boolean option to facet the boxplots into separate charts.

```python
from magmaviz.boxplot import boxplot
boxplot(cars, 'Miles_per_Gallon', 'Origin', facet='Cylinders')
```

### Correlation Plot

Returns a correlation plot based on the numerical features present in the data frame. While the default plot would use circle shapes, an auxiliary input provides the flexibility to switch to square shapes. Additionally, it will print the correlated numerical feature pairs along with their correlation values.

```python
from magmaviz.corrplot import corrplot
corrplot(df, print_corr=True, shape="square")
```

### Histogram

Returns a histogram based on the data frame and a categorical feature to plot on the x-axis. The y-axis will display the result of some of the following aggregating functions:
- Average
- Count
- Distinct
- Max
- Min
- Median
- Mean
- Among others (listed in documentation for the function).

```python
from magmaviz.histogram import histogram
histogram(mtcars, "cars", "count()")
```

### Scatterplot

Returns a scatterplot based on the data frame and two numerical feature names passed as the required inputs. There are auxiliary inputs that provide the flexibility to:
- Color code or change the shape of the data points on a categorical variable
- Set a title to the plot, x-axis, y-axis and color legend
- Change the opacity and size of the data points
- Set the scale of the x-axis and y-axis to start from zero

```python
from magmaviz.scatterplot import scatterplot
scatterplot(df, x, y, c="", t="", o=1.0, s=50, xtitle="", ytitle="", ctitle="", xzero=False, yzero=False, shapes=True)
```

### Fit within the Python ecosystem

Our package will build onto the existing features of 'Altair' using the magma color scheme. It serves as an automated plotter and is a higher level implementation of it. Essentially it circumvents the need to code every single detail and allows the user to focus on the output. We came across two packages that have a similar line of thought:

- [deneb](https://pypi.org/project/deneb/) (Altair) - uses the same base as this package
- [spartan-viz](https://pypi.org/project/spartan-viz/) (Matplotlib) - same philosophy as this package: focus on good use of color


## Contributing

The primary contributors to this package are:

1. Abdul Moid Mohammed
2. Mukund Iyer
3. Irene Yan
4. Rubén De la Garza Macías

We welcome new ideas and contributions. Please refer to the contributing guidelines in the CONTRIBUTING.MD file. Do note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`magmaviz` was created by Abdul Moid Mohammed, Mukund Iyer, Irene Yan, Rubén De la Garza Macías. It is licensed under the terms of the MIT license.

## Credits

`magmaviz` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
