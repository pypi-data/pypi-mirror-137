"""Wraps a very fast rust implementation of polynomials."""

from . import FloatExpression
import numpy as np
class Polynomial:
    """Power-series representation of an n-dimensional polynomial.
    Supports array evaluation, addition, multiplication, composition,
    derivation, and integration."""

    __slots__ = ["_expr"]

    def __init__(self, coef):
        coef = np.array(coef, dtype=np.float64)
        self._expr = FloatExpression(coef)

    def __nonzero__(self):
        return np.any(self.coef)
