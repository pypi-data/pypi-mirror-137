# Copyright 2021 Cognite AS
from .gaps_identification import (
    gaps_identification_iqr,
    gaps_identification_modified_z_scores,
    gaps_identification_z_scores,
)
from .negative_running_hours import negative_running_hours_check
from .outliers import extreme


TOOLBOX_NAME = "Data quality"

__all__ = [
    "gaps_identification_z_scores",
    "gaps_identification_modified_z_scores",
    "gaps_identification_iqr",
    "extreme",
    "negative_running_hours_check",
]
