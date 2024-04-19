#!/usr/bin/env python3
"""Basic annotations - zoom_array"""

from typing import Tuple, List, Union


def zoom_array(lst: Tuple, factor: int = 2) -> Tuple:
    zoomed_in: List = [
        item for item in lst
        for i in range(factor)
    ]
    return zoomed_in
