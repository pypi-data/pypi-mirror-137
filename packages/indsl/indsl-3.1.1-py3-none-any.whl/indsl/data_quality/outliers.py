# Copyright 2021 Cognite AS
import numpy as np
import pandas as pd

from scipy.stats import t as student_dist

from ..exceptions import UserValueError
from ..type_check import check_types


@check_types
def extreme(data: pd.Series, alpha: float = 0.05, bc_relaxation: float = 1.0, poly_order: int = 3):
    """Extreme outliers removal

    Outlier detector and removal based on the `paper from Gustavo A. Zarruk
    <https://iopscience.iop.org/article/10.1088/0957-0233/16/10/012/meta>`_. The procedure is as follows:

         * Fit a polynomial curve to the model using all of the data
         * Calculate the studentized deleted (or externally studentized) residuals
         * These residuals follow a t distribution with degrees of freedom n - p - 1
         * Bonferroni critical value can be computed using the significance level (alpha) and t distribution
         * Any values that fall outside of the critical value are treated as anomalies

    Use of the hat matrix diagonal allows for the rapid calculation of deleted residuals without having to refit
    the predictor function each time.

    Args:
        data (pandas.Series): Time series.
        alpha (float, optional): Significance level.
        bc_relaxation (float, optional): Factor.
            Relaxation factor for the Bonferroni critical value. Smaller values will make anomaly detection more
            conservative. Defaults to 1
        poly_order (int, optional): Polynomial order.
            Order of the polynomial used for the regression function

    Returns:
        pandas.Series: Time series without outliers.

    Raises:
        UserValueError: Alpha needs to be betwen 0 and 1
    """

    # Check inputs
    data = data.dropna()
    if len(data) < 3:
        raise RuntimeError(f"Not enough data (got {len(data)} values) to perform operation (min 3 values required!)")

    if not 0 < alpha < 1:
        raise UserValueError("Alpha needs to be a float between 0 and 1")

    # Convert datetime index to integers
    x = (np.array(data.index, dtype=np.int64) - data.index[0].value) / 1e9
    y = data.to_numpy()  # Just to please pandas devs

    # Create a polynomial fit and apply the fit to data
    coefs = np.polyfit(x, y, poly_order)
    y_pred = np.polyval(coefs, x)

    # Calculate hat matrix
    X_mat = np.vstack((np.ones_like(x), x)).T
    X_hat = X_mat @ np.linalg.inv(X_mat.T @ X_mat) @ X_mat.T
    hat_diagonal = X_hat.diagonal()

    # Calculate degrees of freedom
    n = len(y)
    dof = n - 3  # Using p = 2 from paper

    # Determine the residuals and standardise them
    res = y - y_pred
    sse = np.sum(res ** 2)
    t_res = res * np.sqrt(dof / (sse * (1 - hat_diagonal) - res))

    # Return p values from Student distribution and calculate Bonferroni critical value
    p_vals = student_dist.sf(t_res, df=dof)
    bc = student_dist.sf(1 - alpha / (2 * n), df=dof) * bc_relaxation

    # Return filtered dataframe with the anomalies removed
    mask = np.logical_and(p_vals >= bc, p_vals <= (1 - bc))
    return pd.Series(y[mask], index=data.index[mask])


# TODO: Add auto-example for the outlier removal function
