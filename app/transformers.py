# CF custom module.

"""
Utilities for transforming data.
"""

from copy import deepcopy
from itertools import filterfalse


def data_extra_cleaner(value, pattern):
    if 'extra' in value:
        value = deepcopy(value)  # Preserve original data, might be used by other extractors.
        value['extra'] = extra_cleaner(value['extra'], pattern)
    return value


def extra_cleaner(value, pattern):
    return '\n'.join(
        filterfalse(pattern.match, value.split('\n'))
    ).strip()
