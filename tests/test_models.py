import numpy as np
import pytest

from imports.physics_models import physics_models
from transport_analysis.models import (
    CONDUCTANCE_QUANTUM_S,
    lifetime_broadening,
    single_level_current,
    thermal_broadening,
)


def test_thermal_peak_is_symmetric_and_reaches_requested_maximum():
    voltage = np.array([-1.0, 0.0, 1.0])

    conductance = thermal_broadening(
        voltage,
        temperature=100,
        center_voltage=0,
        peak_conductance=2.5,
        gate_coupling=0.01,
    )

    assert conductance[0] == pytest.approx(conductance[2])
    assert conductance[1] == pytest.approx(2.5)


def test_lifetime_peak_has_expected_center_value():
    conductance = lifetime_broadening(
        [0.0],
        center_voltage=0,
        broadening=0.01,
        gate_coupling=0.1,
    )

    assert conductance[0] == pytest.approx(4 * CONDUCTANCE_QUANTUM_S)


def test_single_level_current_is_zero_at_zero_bias():
    current = single_level_current(
        [-1, 0, 1],
        0,
        prefactor=1,
        center_voltage=0,
        gate_coupling=0.1,
        source_coupling=0.5,
        temperature=4,
    )

    np.testing.assert_allclose(current, 0)


def test_legacy_thermal_model_delegates_to_public_model():
    expected = thermal_broadening(
        [-0.5, 0, 0.5],
        temperature=10,
        center_voltage=0,
        peak_conductance=1,
        gate_coupling=0.01,
    )

    actual = physics_models.thermal_broadening(
        np.array([-0.5, 0, 0.5]),
        10,
        0,
        1,
        0.01,
    )

    np.testing.assert_allclose(actual, expected)
