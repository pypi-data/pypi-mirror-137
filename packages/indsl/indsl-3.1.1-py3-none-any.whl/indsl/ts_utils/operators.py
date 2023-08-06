# Copyright 2021 Cognite AS
import operator as op

import numpy as np

# Simple operations
import pandas as pd

from indsl.resample.auto_align import auto_align
from indsl.type_check import check_types


@check_types
def add(a, b, align_timesteps: bool = False):
    """Add
    Add any two time series or numbers.

    Args:
        a: Time-series or number.
        b: Time-series or number.
        align_timesteps (bool) : Auto-align
            Automatically align time stamp  of input time series. Default is False.

    Returns:
        pandas.Series: time series
    """
    a, b = auto_align([a, b], align_timesteps)
    return op.add(a, b)


@check_types
def sub(a, b, align_timesteps: bool = False):
    """Subtraction
    The difference between two time series or numbers.

    Args:
        a: Time-series or number.
        b: Time-series or number.
        align_timesteps (bool) : Auto-align
           Automatically align time stamp  of input time series. Default is False.

    Returns:
        pandas.Series: time series
    """
    a, b = auto_align([a, b], align_timesteps)
    return op.sub(a, b)


@check_types
def mul(a, b, align_timesteps: bool = False):
    """Multiplication
    Multiply two time series or numbers.

    Args:
        a: Time-series or number.
        b: Time-series or number.
        align_timesteps (bool): Auto-align
           Automatically align time stamp  of input time series. Default is False.

    Returns:
        pandas.Series: time series
    """
    a, b = auto_align([a, b], align_timesteps)
    return op.mul(a, b)


@check_types
def div(a, b, align_timesteps: bool = False):
    """Division
    Divide two time series or numbers. If the time series in the denominator contains zeros,
    all instances are dropped from the final result.

    Args:
        a: Numerator
        b: Denominator
        align_timesteps (bool): Auto-align
           Automatically align time stamp  of input time series. Default is False.

    Returns:
        pandas.Series: time series
    """

    a, b = auto_align([a, b], align_timesteps)

    if type(b) is pd.Series:
        res = op.truediv(a, b).replace([np.inf, -np.inf], np.nan).dropna()
    elif type(b) is np.array:
        b = b.astype("float")  # Make sure it is a float to replace zeros (int) by np.nan (float)
        b[b == 0] = np.nan
        res = op.truediv(a, b)
        res = res[~np.isnan(res)]
    else:
        res = op.truediv(a, b)

    return res


@check_types
def power(a, b, align_timesteps: bool = False):
    """Power
    Power of time series or numbers.

    Args:
        a: base time series or number
        b: exponent time series or number
        align_timesteps (bool): Auto-align
           Automatically align time stamp  of input time series. Default is False.

    Returns:
        pandas.Series: time series
    """
    a, b = auto_align([a, b], align_timesteps)
    return op.pow(a, b)


def inv(x):
    """Inverse
    Element-wise inverse of time series or numbers

    Args:
        x: time series or numbers

    Returns:
        pandas.Series: time series
    """
    return 1 / x


def sqrt(x):
    """Square root
    Square root of time series or numbers

    Args:
        x: time series or numbers

    Returns:
        pandas.Series: time series
    """
    return np.sqrt(x)


def neg(x):
    """Negation
    Negation of time series or numbers

    Args:
        x: time series or numbers

    Returns:
        pandas.Series: time series
    """
    return op.neg(x)


def absolute(x):
    """Absolute value
    Absolute value of time series or numbers

    Args:
        x: time series or numbers

    Returns:
        pandas.Series: time series
    """
    return op.abs(x)


@check_types
def mod(a, b, align_timesteps: bool = False):
    """Modulo
    Modulo of time series or numbers

    Args:
        a: dividend time series or number
        b: divisor time series or number
        align_timesteps (bool): Auto-align
           Automatically align time stamp  of input time series. Default is False.

    Returns:
        pandas.Series: time series
    """
    a, b = auto_align([a, b], align_timesteps)
    return op.mod(a, b)
