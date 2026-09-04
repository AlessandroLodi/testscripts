import numpy as np
import pytest

from transport_analysis import differentiate, fit_polynomial


def test_differentiate_returns_midpoints_and_derivative():
    x = np.array([0.0, 1.0, 3.0])
    y = x**2

    midpoints, derivative = differentiate(x, y)

    np.testing.assert_allclose(midpoints, [0.5, 2.0])
    np.testing.assert_allclose(derivative, [1.0, 4.0])


def test_differentiate_rejects_repeated_x_values():
    with pytest.raises(ValueError, match="duplicates"):
        differentiate([0, 0], [1, 2])


def test_fit_polynomial_returns_standard_coefficients():
    x = np.linspace(-2, 2, 20)
    y = 3 * x**2 - 2 * x + 4

    result = fit_polynomial(x, y, degree=2)

    np.testing.assert_allclose(result.coefficients, [3, -2, 4], atol=1e-12)
    assert result.degree == 2
    assert result.sample_count == 20
    assert result.rms_residual < 1e-12


def test_fit_polynomial_validates_sample_count():
    with pytest.raises(ValueError, match="requires at least"):
        fit_polynomial([1, 2], [3, 4], degree=2)
