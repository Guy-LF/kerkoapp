# CF custom module.

"""
Utilities for transforming data.
"""

from copy import deepcopy
from itertools import filterfalse


def clean_data_extra(value, pattern):
    if 'extra' in value:
        value = deepcopy(value)  # Preserve original data, might be used by other extractors.
        value['extra'] = clean_string(value['extra'], pattern)
    return value


def clean_string(value, pattern):
    """Remove from a string value the lines that match the given pattern."""
    return '\n'.join(
        filterfalse(pattern.match, value.split('\n'))
    ).strip()
