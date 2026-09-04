"""Compact transport models used by the stability-diagram analyses.

Energies are expressed in electronvolts, voltages in volts, temperatures in
kelvin, and conductance in siemens unless a function says otherwise.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy.special import expit


BOLTZMANN_EV_PER_K = 8.617_333_262e-5
CONDUCTANCE_QUANTUM_S = 7.748_091_729e-5


def thermal_broadening(
    gate_voltage: ArrayLike,
    *,
    temperature: float,
    center_voltage: float,
    peak_conductance: float,
    gate_coupling: float,
) -> NDArray[np.float64]:
    """Return a thermally broadened Coulomb peak.

    ``gate_coupling`` is the gate lever arm in eV/V. The stable logistic form
    below is equivalent to ``peak_conductance / cosh(x)**2``.
    """

    if temperature <= 0:
        raise ValueError("temperature must be positive")
    voltage = np.asarray(gate_voltage, dtype=float)
    argument = gate_coupling * (voltage - center_voltage) / (
        BOLTZMANN_EV_PER_K * temperature
    )
    sech_squared = 4 * expit(argument) * expit(-argument)
    return np.asarray(peak_conductance * sech_squared, dtype=float)


def lifetime_broadening(
    gate_voltage: ArrayLike,
    *,
    center_voltage: float,
    broadening: float,
    gate_coupling: float,
    conductance_quantum: float = CONDUCTANCE_QUANTUM_S,
) -> NDArray[np.float64]:
    """Return a lifetime-broadened Lorentzian conductance peak."""

    if broadening <= 0:
        raise ValueError("broadening must be positive")
    voltage = np.asarray(gate_voltage, dtype=float)
    broadening_squared = broadening**2
    denominator = broadening_squared / 4 + (
        gate_coupling * (voltage - center_voltage)
    ) ** 2
    return np.asarray(
        conductance_quantum * broadening_squared / denominator,
        dtype=float,
    )


def single_level_current(
    gate_voltage: ArrayLike,
    bias_voltage: ArrayLike,
    *,
    prefactor: float,
    center_voltage: float,
    gate_coupling: float,
    source_coupling: float,
    temperature: float,
) -> NDArray[np.float64]:
    """Return the sequential-tunnelling current through one molecular level.

    Gate and bias arrays follow NumPy broadcasting rules, which supports both
    one-dimensional traces and two-dimensional stability-diagram grids.
    """

    if temperature <= 0:
        raise ValueError("temperature must be positive")
    gate = np.asarray(gate_voltage, dtype=float)
    bias = np.asarray(bias_voltage, dtype=float)
    chemical_potential = (
        gate_coupling * center_voltage
        - gate_coupling * gate
        - source_coupling * bias
    )
    thermal_energy = BOLTZMANN_EV_PER_K * temperature
    drain_occupation = expit(-chemical_potential / thermal_energy)
    source_occupation = expit(-(chemical_potential + bias) / thermal_energy)
    return np.asarray(
        prefactor * (drain_occupation - source_occupation),
        dtype=float,
    )
