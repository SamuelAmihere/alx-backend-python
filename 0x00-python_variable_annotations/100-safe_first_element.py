#!/usr/bin/env python3
"""AI is creating summary for this file"""
from typing import List, Union


def safe_first_element(lst: List[Union[int, float]]) -> Union[int, float, None]:
    """Duck-typed annotations"""
    if lst:
        return lst[0]
    else:
        return None
