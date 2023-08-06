# Copyright 2021 Cognite AS
from .simple_filters import status_flag_filter
from .wavelet_filter import wavelet_filter


__all__ = ["wavelet_filter", "status_flag_filter"]

TOOLBOX_NAME = "Filter"
