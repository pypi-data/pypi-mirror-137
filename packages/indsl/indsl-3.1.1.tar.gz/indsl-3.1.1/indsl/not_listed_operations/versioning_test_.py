# Copyright 2021 Cognite AS
import pandas as pd

from indsl.versioning import register


@register(version="0.0", deprecated=True, deprecation_warning="Function is deprecated")
def versioning_test_op(series: pd.Series):
    """Old versioning test
    This old function is used only for testing purposes

    Args:
        series: Dummy input

    Returns:
        pandas.Series: Dummy output
    """
    return series
