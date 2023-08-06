# Copyright 2021 Cognite AS

from typing import List, Literal, Optional

import numpy as np
import pandas as pd

from indsl.resample.auto_align import auto_align

from ..exceptions import UserValueError
from ..type_check import check_types


TimeUnits = Literal["ns", "us", "ms", "s", "m", "h", "D", "W"]


# Rounding and utility functions
@check_types
def round(x, decimals: int):
    """Round
    Rounds a time series to a given number of decimals

    Args:
        x: time series
        decimals (int): number of decimals

    Returns:
        pandas.Series: time series
    """
    return np.round_(x, decimals=decimals)


def floor(x):
    """Round down
    Rounds a time series down to the nearest integer smaller than or equal to the current value

    Args:
        x: time series

    Returns:
        pandas.Series: time series
    """
    return np.floor(x)


def ceil(x):
    """Round up
    Rounds a time series up to the nearest integer greater than or equal to the current value

    Args:
        x: time series

    Returns:
        pandas.Series: time series
    """
    return np.ceil(x)


def sign(x):
    """Sign
    Element-wise indication of the sign of a time series

    Args:
        x: time series

    Returns:
        pandas.Series: time series
    """
    return np.sign(x)


# Clipping functions
@check_types
def clip(x, low: float = -np.inf, high: float = np.inf):
    """Clip(low, high)
    Given an interval, values of the time series outside the interval are clipped to the interval edges.

    Args:
        x (pandas.Series): time series
        low (float, Optional): Lower limit
            Lower clipping limit. Default: -infinity
        high (float, Optional): Upper limit
            Upper clipping limit. Default: +infinity

    Returns:
        pandas.Series: time series
    """
    return np.clip(x, low, high)


@check_types
def maximum(x1, x2, align_timesteps: bool = False):
    """Element-wise maximum
    Computes the maximum value of two timeseries or numbers

    Args:
        x1: First time series or number
        x2: Second time series or number
        align_timesteps (bool) : Auto-align
          Automatically align time stamp  of input time series. Default is False.

    Returns:
        pandas.Series: time series
    """
    x1, x2 = auto_align([x1, x2], align_timesteps)
    return np.maximum(x1, x2)


@check_types
def minimum(x1, x2, align_timesteps: bool = False):
    """Element-wise minimum
    Computes the minimum value of two timeseries

    Args:
        x1: First time series or number
        x2: Second time series or number
        align_timesteps (bool) : Auto-align
          Automatically align time stamp  of input time series. Default is False.

    Returns:
        pandas.Series: time series
    """
    x1, x2 = auto_align([x1, x2], align_timesteps)
    return np.minimum(x1, x2)


@check_types
def union(series1: pd.Series, series2: pd.Series) -> pd.Series:
    """Union
    Takes the union of two time series. If a time stamp
    occurs in both series, the value of the first time series is used.

    Args:
        series1 (pd.Series): time series
        series2 (pd.Series): time series

    Returns:
        pandas.Series: time series

    Raises:
        UserTypeError: series1 or series2 is not a time series
    """

    out = series1.append(series2).sort_index()
    return out[~out.index.duplicated(keep="first")]


@check_types
def bin_map(x1, x2, align_timesteps: bool = False):
    """Element-wise greater-than
    Maps to a binary array by checking if one timeseries is greater than another

    Args:
        x1: First time series or number
        x2: Second time series or number
        align_timesteps (bool): Auto-align
          Automatically align time stamp  of input time series. Default is False.

    Returns:
        np.ndarray: time series
    """
    x1, x2 = auto_align([x1, x2], align_timesteps)
    return out.astype(np.int64) if hasattr(out := x1 > x2, "astype") else out


@check_types
def set_timestamps(timestamp_series: pd.Series, value_series: pd.Series, unit: TimeUnits = "ms") -> pd.Series:
    """Set index of time series
    Sets the time series values to the Unix timestamps.
    The timestamps follow the Unix convention (Number of seconds
    starting from January 1st, 1970). Both input time series
    must have the same length.


    Args:
        timestamp_series (pd.Series): Timestamp time series
        value_series (pd.Series): Value time series
        unit (str): Timestamp unit
          Valid values "ns|us|ms|s|m|h|D|W". Default "ms"

    Returns:
        pd.Series: time series

    Raises:
        UserTypeError: timestamp_series or value_series are not time series
        UserTypeError: unit is not a string
        UserValueError: timestamp_series and value_series do not have the same length
    """
    if not len(timestamp_series) == len(value_series):
        raise UserValueError("Length of input time series must be equal.")

    index = pd.to_datetime(timestamp_series.to_numpy(), unit=unit)
    return pd.Series(value_series.to_numpy(), index=index)


@check_types
def get_timestamps(series: pd.Series, unit: TimeUnits = "ms") -> pd.Series:
    """Get index of time series

    Get timestamps of the time series as values.
    The timestamps follow the Unix convention (Number of seconds
    starting from January 1st, 1970). Precision loss in the order of
    nanoseconds may happen if unit is not nanoseconds.

    Args:
        series (pd.Series): Time-series
        unit (str): Timestamp unit
          Valid values "ns|us|ms|s|m|h|D|W". Default "ms"

    Returns:
        pd.Series: time series

    Raises:
        UserTypeError: series is not a time series
        UserTypeError: unit is not a string
    """
    if unit == "ns":
        values = series.index.to_numpy("datetime64[ns]").view(np.int64)
    else:
        values = series.index.view(np.int64) / pd.Timedelta(1, unit=unit).value

    return pd.Series(values, index=series.index)


@check_types
def time_shift(series: pd.Series, n_units: float = 0, unit: TimeUnits = "ms") -> pd.Series:
    """Shift time series

    Shift time series by a time period

    Args:
        series (pd.Series): Time-series
        n_units (float): Time periods to shift
            Number of time periods to shift
        unit (str): Time period unit
          Valid values "ns|us|ms|s|m|h|D|W". Default "ms"

    Returns:
        pd.Series: time series

    Raises:
        UserTypeError: series is not a time series
        UserTypeError: n_units is not a number
        UserTypeError: unit is not a string
    """
    out = series.copy()
    out.index += pd.Timedelta(n_units, unit=unit)

    return out


@check_types
def replace(series: pd.Series, to_replace: Optional[List[float]] = None, value: Optional[float] = 0.0):
    """Replace
    Replace values in a time series. The values to replace should be a semicolon-separated list.
    Undefined and infinity values can be replaced by using nan, inf and -inf (e.g. 1.0, 5, inf, -inf, 20, nan).

    Args:
        series (pd.Series): Time series
        to_replace (List[float], optional): Replace
            List of values to replace. The values must be seperated by semicolons. Infinity and undefined values can be
            replaced by using the keywords inf, -inf and nan. The default is to replace no values.
        value (float, optional): By
            Value used as replacement. Default is 0.0

    Returns:
        pd.Series: time series

    Raises:
        UserTypeError: series is not a time series
        UserTypeError: to_replace is not a list
        UserTypeError: value is not a number

    """
    if to_replace is None:
        return series
    return series.replace(to_replace, value)


@check_types
def remove(series: pd.Series, to_remove: Optional[List[float]] = None):
    """Remove
    Remove values in a time series. The values to remove should be a semicolon-separated list.
    Undefined and infinity values can be replaced by using nan, inf and -inf (e.g. 1.0, 5, inf, -inf, 20, nan).


    Args:
        series (pd.Series): Time series
        to_remove (List[float], optional): Remove
            List of values to remove. The values must be seperated by semicolons. Infinity and undefined values can be
            replaced by using the keywords inf, -inf and nan.

    Returns:
        pd.Series: time series

    Raises:
        UserTypeError: series is not a time series
        UserTypeError: to_remove is not a list
    """
    if to_remove is None:
        return series
    return series[~series.isin(to_remove)]


@check_types
def threshold(series: pd.Series, low: float = -np.inf, high: float = np.inf):
    """Threshold
    Indicates if the input series exceeds the lower and higher limits. The output series
    is 1.0 if the input is between the (inclusive) limits, and 0.0 otherwise.

    Args:
        series (pandas.Series): Time series
        low (float, Optional): Lower limit
           threshold. Default: -infinity
        high (float, Optional): Upper limit
           threshold. Default: +infinity

    Returns:
        pd.Series: Time series

    Raises:
        UserTypeError: series is not a time series
        UserTypeError: low or high are not floats
    """
    return series.between(low, high).astype(np.int64)
