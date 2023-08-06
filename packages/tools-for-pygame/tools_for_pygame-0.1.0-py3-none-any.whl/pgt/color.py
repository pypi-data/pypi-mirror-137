#!/usr/bin/env python3

from numbers import Real
from typing import List

from .mathf import clamp
from .type_hints import _col_type


def add_col(col1: _col_type, col2: _col_type) -> List[int]:
    return [clamp(c1 + c2, 0, 255) for c1, c2 in zip(col1, col2)]


def sub_col(col1: _col_type, col2: _col_type) -> List[int]:
    return [clamp(c1 - c2, 0, 255) for c1, c2 in zip(col1, col2)]


def mul_col(col1: _col_type, col2: _col_type) -> List[int]:
    return [clamp(c1 * c2, 0, 255) for c1, c2 in zip(col1, col2)]


def min_col(col1: _col_type, col2: _col_type) -> List[int]:
    return [min(c1, c2) for c1, c2 in zip(col1, col2)]


def max_col(col1: _col_type, col2: _col_type) -> List[int]:
    return [max(c1, c2) for c1, c2 in zip(col1, col2)]


def calc_alpha(new_color: _col_type, prev_color: _col_type, alpha: Real) -> List[int]:
    return [alpha * c1 + (1 - alpha) * c2 for c1, c2 in zip(new_color, prev_color)]


GRAY = lambda c: (clamp(c, 0, 255), clamp(c, 0, 255), clamp(c, 0, 255), 255)

R = lambda c: (clamp(c, 0, 255), 0, 0, 255)

G = lambda c: (0, clamp(c, 0, 255), 0, 255)

B = lambda c: (0, 0, clamp(c, 0, 255), 255)
