# Copyright 2021 Cognite AS

import numpy as np
import pandas as pd

from scipy.stats import shapiro

from ..exceptions import UserValueError
from ..type_check import check_types, validate_time_series_format


def _validate_inputs(x: pd.Series):
    validate_time_series_format(x)

    if len(x) == 0:
        raise UserValueError("Time series is empty.")


def _generate_step_series(index: pd.Index, is_gap: np.array) -> pd.Series:
    """Construct a step-wise time series (with 0-1 values) from an index and a boolean list"""

    # Identify the timestamp indices where the gaps start and stop
    gap_start_indices = np.where(~is_gap[:-1] & is_gap[1:])[0] + 1
    gap_stop_indices = np.where(is_gap[:-1] & ~is_gap[1:])[0] + 1

    # Add values for the first and last time stamp
    new_index = index[:1].append(index[-1:])
    data = [1 if is_gap[0] else 0, 1 if is_gap[-1] else 0]

    # Add a 0-1 flank for all gap starts
    new_index = new_index.append(index[gap_start_indices])
    data += [0] * len(gap_start_indices)

    new_index = new_index.append(index[gap_start_indices] + pd.Timedelta(1, unit="ms"))
    data += [1] * len(gap_start_indices)

    # Add a 1-0 flank for all gap stops
    new_index = new_index.append(index[gap_stop_indices])
    data += [1] * len(gap_stop_indices)

    new_index = new_index.append(index[gap_stop_indices] + pd.Timedelta(1, unit="ms"))
    data += [0] * len(gap_stop_indices)

    return pd.Series(data, index=new_index).sort_index()


@check_types
def gaps_identification_z_scores(
    x: pd.Series, cutoff: float = 3.0, test_normality_assumption: bool = False
) -> pd.Series:
    """Gaps detection, Z-scores

    Detect gaps in the time stamps using `Z-scores <https://en.wikipedia.org/wiki/Standard_score>`_. Z-score stands for
    the number of standard deviations by which the value of a raw score (i.e., an observed value or data point) is
    above or below the mean value of what is being observed or measured. This method assumes that the time step sizes
    are normally distributed. Gaps are defined as time periods where the Z-score is larger than cutoff.

    Args:
        x (pandas.Series): Time series
        cutoff (float, optional): Cut-off
            Time periods are considered gaps if the Z-score is over this cut-off value. Default 3.0.
        test_normality_assumption (bool, optional): Test for normality
            Raise a warning if the data is not normally distributed.
            The Shapiro-Wilk test is used. The test is only performed if the the time series contains at least 50 data points.

    Returns:
        pandas.Series: Time series
            The returned time series is an indicator function that is 1 where there is a gap, and 0 otherwise.

    Raises:
        UserTypeError: x is not a time series
        UserTypeError: cutoff is not a number
        UserValueError: x is empty
        UserValueError: time steps of time series are not normally distributed
    """
    _validate_inputs(x)

    if len(x) < 2:
        return pd.Series([0] * len(x), index=x.index)

    timestamps = x.index.to_numpy(np.int64)
    diff = np.diff(timestamps)

    if test_normality_assumption and len(x) >= 50:
        W, p_value = shapiro(diff)
        # W is between 0 and 1, small values lead to a rejection of the
        # normality assumption. Ref: https://www.nrc.gov/docs/ML1714/ML17143A100.pdf
        if len(x) < 5000 and p_value < 0.05 or W < 0.5:
            raise UserValueError("The time steps are not normally distibuted")

    if (std := diff.std()) == 0.0:
        z_scores = np.zeros(len(diff))
    else:
        z_scores = (diff - diff.mean()) / std

    is_gap = np.where(z_scores > cutoff, True, False)

    return _generate_step_series(x.index, is_gap)


@check_types
def gaps_identification_modified_z_scores(x: pd.Series, cutoff: float = 3.5) -> pd.Series:
    """Gaps detection, mod. Z-scores

    Detect gaps in the time stamps using modified Z-scores. Gaps are defined as time periods
    where the Z-score is larger than cutoff.

    Args:
        x (pandas.Series): Time series
        cutoff (float, optional): Cut-off
            Time-periods are considered gaps if the modified Z-score is over this cut-off value. Default 3.5.

    Returns:
        pandas.Series: Time series
            The returned time series is an indicator function that is 1 where there is a gap, and 0 otherwise.

    Raises:
        UserTypeError: x is not a time series
        UserTypeError: cutoff has to be of type float
        UserValueError: x is empty
        UserValueError: time steps of time series are not normally distributed
    """
    _validate_inputs(x)

    if len(x) < 2:
        return pd.Series([0] * len(x), index=x.index)

    timestamps = x.index.to_numpy(np.int64)
    diff = np.diff(timestamps)

    median = np.median(diff)
    if (mad := np.median(np.abs(diff - median))) == 0.0:
        modified_z_scores = np.zeros(len(diff))
    else:
        modified_z_scores = 0.6745 * (diff - median) / mad

    is_gap = np.where(modified_z_scores > cutoff, True, False)

    return _generate_step_series(x.index, is_gap)


@check_types
def gaps_identification_iqr(x: pd.Series) -> pd.Series:
    """Gaps detection, IQR

    Detect gaps in the time stamps using the `interquartile range (IQR)
    <https://en.wikipedia.org/wiki/Interquartile_range>`_ method. The IQR is a measure of statistical
    dispersion, which is the spread of the data. Any time steps that are more than 1.5 IQR above Q3 are considered
    gaps in the data.

    Args:
        x (pandas.Series): time series

    Returns:
        pandas.Series: time series
            The returned time series is an indicator function that is 1 where there is a gap, and 0 otherwise.

    Raises:
        UserTypeError: x is not a time series
        UserValueError: x is empty
    """
    _validate_inputs(x)

    if len(x) < 2:
        return pd.Series([0] * len(x), index=x.index)

    timestamps = x.index.to_numpy(np.int64)
    diff = np.diff(timestamps)

    percentile25 = np.quantile(diff, 0.25)
    percentile75 = np.quantile(diff, 0.75)

    iqr = percentile75 - percentile25
    upper_limit = percentile75 + 1.5 * iqr
    is_gap = np.where(diff > upper_limit, True, False)

    return _generate_step_series(x.index, is_gap)
