# CF custom module.

"""
Utilities for transforming data.
"""

from copy import deepcopy
from itertools import filterfalse


def clean_data_extra(value, pattern):
    if "extra" in value:
        # Preserve original data, might be used by other extractors.
        value = deepcopy(value)
        value["extra"] = clean_lines(value["extra"], pattern)
    return value


def clean_lines(value, pattern):
    """Remove from a string value the lines that match the given pattern."""
    if not isinstance(value, str):
        return value
    return "\n".join(filterfalse(pattern.match, value.split("\n"))).strip()
