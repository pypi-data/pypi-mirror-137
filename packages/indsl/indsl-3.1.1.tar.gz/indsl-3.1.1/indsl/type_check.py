from functools import wraps

import pandas as pd

from typeguard import typechecked

from indsl.exceptions import UserTypeError


def error_handling(operation):
    """Decorator that catches TypeError and wraps to inDSL specific error """

    @wraps(operation)
    def wrapper(*args, **kwargs):
        try:
            return operation(*args, **kwargs)
        except TypeError as e:
            raise UserTypeError(str(e)) from e

    return wrapper


def check_types(operation):
    """Decorator to check types of inputs and outputs of a function

    Decorator uses typeguard library to validate arguments of a function,
    and then wraps a TypeError to UserTypeError which is specific for inDSL library
    """
    return error_handling(typechecked(operation))


def validate_time_series_format(data: pd.Series):
    """Helper method to validate if provided pandas.Series is of type pandas.DatetimeIndex"""
    if not isinstance(data.index, pd.DatetimeIndex):
        raise UserTypeError(f"Expected a time series, got index type {data.index.dtype}")
