# lrasm

# Package for testing linear and multiple linear regression assumptions


This package is built to contain functions to be able to quickly and easily test the linearity assumptions befre preforming linear regression or multiple linear regression for a specified dataset. 

The three assumptions should be satisfied to ensure the effectiveness of a linear regression model for a particular dataset and are described as follows:

-   **No Multicollinearity**: individual predictors within a model should not be linearly correlated to avoid unstable linear estimators

-   **Constant Variance of Residuals (homoscedasticity)**: Since data should be individually and identically distributed, the residuals should be independent of fitted values

-   **Normality of residuals**: Since the conditional expectation of the predicted value should be normal, the error terms of the resulting model should also be normally distributed

The package contains 3 functions one for checking multicolliniarity, one for checking constant variance and one for checking normality in the residuals.

Function 1: Multicolliniarity.

- Takes in a pandas dataframe and a VIF threshold and checks if any of the calculated vif values exceed the given threshold. If so, the function will advise the user that this assumtion is violated, and vice versa.

- Returns the Calculated VIF values and a statement telling the user whether or not the assumpton is violated.

Function 2: Constant Variance.

- Takes in a pandas dataframe containing predictors, a pandas series containing the response, and a variability threshold and checks if the variabiliy of the residuals is contant by comparing it to the given threshold. If the threshold is exceeded the function will advise the user that this assumtion is violated, and vice versa.

- Returns a plot of the fitted values vs residuals, the calculated variability value  and a statement telling the user whether or not the assumpton is violated.

Function 3: Normality.

- Takes in a pandas dataframe containing predictors, a pandas series containing the response, and a P-value threshold, and preforms a shapiro wilk test for normality. If the P-value of the test does not exceed the threshold, the function will advise the user that this assumtion is violated, and vice versa.

- Returns the Calculated P-value and a statement telling the user whether or not the assumpton is violated.

## Installation

```bash
$ pip install git+https://github.com/UBC-MDS/lrasm
```

## Usage

Examples for usage and further documentation on ReadtheDocs can be found here: https://lrasm.readthedocs.io/en/latest/

`lrasm` can be used to check linear regression assumptions as follows:

```
from lrasm.homoscedasticity_tst import homoscedasticity_test
from lrasm.multicollinearity_tst import multicollinearity_test
from lrasm.normality_tst import normality_test
from sklearn import datasets
import pandas as pd
import matplotlib.pyplot as plt

# Import/Process Test data:

data = datasets.load_iris()
iris_df = pd.DataFrame(data=data.data, columns=data.feature_names)
X = iris_df.drop("sepal width (cm)", axis = 1)
y = iris_df["petal width (cm)"]

# Test for Normality:

p_value, res = normality_test(X, y)

# Test for Homoscedasticity:

corr_df, plot = homoscedasticity_test(X, y)

# Test for Multicollinearity:

vif_df = multicollinearity_test(X, VIF_thresh = 10)
```

## Ecosystem

As of January 2022, there are no other packages that we have found which explicitly evaluate the assumptions made by linear regression. The LR_assumption_test package seeks to fill in this gap and build upon existing python packages. This package aggregates the functions offered by scikit-learn, statsmodels, scipy.stats, matplotlib and more, seeking to build upon them for the purpose of evaluating linear regression models. This is intended to make it more accessible for users to access the functionality of the previously mentioned packages, as well as improve the clarity of results.

## Contributing

Authors: Yair Guterman, Hatef Rahmani, Song Bo Andy Yang  
Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`lrasm` was created by Yair Guterman, Hatef Rahmani, Song Bo Andy Yang . It is licensed under the terms of the MIT license.

## Credits
`lrasm` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
