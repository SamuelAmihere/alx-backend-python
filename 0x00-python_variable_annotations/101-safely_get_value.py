#!/usr/bin/env python3
"""More involved type annotations"""

from typing import Union, Any, TypeVar

T = TypeVar('T')
DEF = Union[int, float, str, bytes, Any, T]
RES = Union[int, float, str, bytes, Any, None]


def safely_get_value(dct: dict, key: Any, default: T = None) -> DEF:
    """Return the value of a key in a dictionary"""
    if key in dct:
        return dct[key]
    else:
        return default
