"""Numerical helpers that do not depend on plotting or project data files."""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np
from numpy.typing import ArrayLike, NDArray


FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class PolynomialFit:
    """Result of a least-squares polynomial fit.

    Coefficients use NumPy's conventional highest-power-first order. For
    example, a linear fit contains ``(slope, intercept)``.
    """

    coefficients: FloatArray
    rms_residual: float
    sample_count: int

    @property
    def degree(self) -> int:
        return len(self.coefficients) - 1

    def predict(self, x: ArrayLike) -> FloatArray:
        """Evaluate the fitted polynomial at *x*."""

        return np.asarray(np.polyval(self.coefficients, x), dtype=float)


def _as_vector(values: ArrayLike, *, name: str) -> FloatArray:
    array = np.asarray(values, dtype=float)
    if array.ndim != 1:
        raise ValueError(f"{name} must be one-dimensional")
    if array.size == 0:
        raise ValueError(f"{name} must not be empty")
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must contain only finite values")
    return array


def differentiate(x: ArrayLike, y: ArrayLike) -> tuple[FloatArray, FloatArray]:
    """Return the first finite difference of *y* and its x midpoints.

    Repeated x values are rejected because their derivative is undefined.
    """

    x_values = _as_vector(x, name="x")
    y_values = _as_vector(y, name="y")
    if x_values.size != y_values.size:
        raise ValueError("x and y must have the same length")
    if x_values.size < 2:
        raise ValueError("at least two samples are required")

    delta_x = np.diff(x_values)
    if np.any(delta_x == 0):
        raise ValueError("x values must not contain adjacent duplicates")

    midpoints = x_values[:-1] + delta_x / 2
    derivative = np.diff(y_values) / delta_x
    return midpoints, derivative


def fit_polynomial(
    x: ArrayLike,
    y: ArrayLike,
    *,
    degree: int = 1,
    sample_range: slice | tuple[int | None, int | None] | None = None,
) -> PolynomialFit:
    """Fit a polynomial and return coefficients plus an RMS residual.

    ``sample_range`` can restrict the fit to a half-open index range without
    requiring callers to duplicate array slicing logic.
    """

    x_values = _as_vector(x, name="x")
    y_values = _as_vector(y, name="y")
    if x_values.size != y_values.size:
        raise ValueError("x and y must have the same length")
    if isinstance(degree, bool) or not isinstance(degree, (int, np.integer)):
        raise TypeError("degree must be an integer")
    if degree < 0:
        raise ValueError("degree must be non-negative")

    if sample_range is not None:
        selected = (
            sample_range
            if isinstance(sample_range, slice)
            else slice(sample_range[0], sample_range[1])
        )
        x_values = x_values[selected]
        y_values = y_values[selected]

    if x_values.size <= degree:
        raise ValueError(f"a degree-{degree} fit requires at least {degree + 1} samples")

    coefficients = np.polyfit(x_values, y_values, degree)
    residuals = y_values - np.polyval(coefficients, x_values)
    rms_residual = float(np.sqrt(np.mean(np.square(residuals))))
    return PolynomialFit(
        coefficients=np.asarray(coefficients, dtype=float),
        rms_residual=rms_residual,
        sample_count=x_values.size,
    )
