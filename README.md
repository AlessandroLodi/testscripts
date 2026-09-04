# Transport analysis tools

Utilities and exploratory analyses for QTLab molecular electronic-transport
data. The reusable API lives in `transport_analysis`; the root-level scripts
and notebooks document past, experiment-specific workflows.

## Set up

Python 3.10 or newer is required. From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install -e '.[test]'
python -m pytest
```

Install `.[fit]` as well when using the optional `lmfit`-based routines in the
legacy QTLab classes.

## Use the reusable API

```python
import numpy as np

from transport_analysis import differentiate, fit_polynomial

gate_voltage = np.linspace(-1.0, 1.0, 101)
current = 2.0 * gate_voltage + 0.1

midpoints, transconductance = differentiate(gate_voltage, current)
fit = fit_polynomial(gate_voltage, current, degree=1)

print(fit.coefficients)   # [slope, intercept]
print(fit.rms_residual)
```

Common transport models are exposed with explicit parameter names and units:

```python
from transport_analysis import thermal_broadening

conductance = thermal_broadening(
    gate_voltage,
    temperature=4.2,          # K
    center_voltage=0.0,       # V
    peak_conductance=1e-8,    # S
    gate_coupling=0.02,       # eV/V
)
```

To discover data using the established QTLab filename format:

```python
from transport_analysis.datasets import find_qtlab_dataset

dataset = find_qtlab_dataset("/path/to/experiment", folders=["eburn"])
stability_diagrams = dataset[dataset["type"] == "IVsVg"]
```

Plotting is explicit and does not change global Matplotlib settings at import
time:

```python
from transport_analysis.plotting import apply_plot_style, plot_trace, save_figure

apply_plot_style()
figure, axes = plot_trace(gate_voltage, current, title="Gate trace")
axes.set(xlabel="Gate voltage (V)", ylabel="Current (A)")
save_figure(figure, "figures/gate_trace", formats=("png", "pdf"))
```

## Repository map

- `transport_analysis/`: maintained numerical, dataset, file, and plotting
  helpers. Prefer these imports in new work.
- `imports/`: the established QTLab data containers, stability-diagram plots,
  and physical models. These retain the historical API used by the notebooks.
- `helper_functions.py` and `plotting_functions.py`: compatibility shims for
  older notebooks.
- root-level `.py` and `.ipynb` files: experiment-specific analyses. Many use
  paths and parameters from the original measurement environment; copy one and
  pass your own paths instead of editing library modules.
- root-level `.csv` and `.xlsx` files: example/result data used by notebooks.

The legacy scripts are intentionally not imported by the package: several run
an analysis immediately and contain machine-specific paths. New shared logic
should be added to `transport_analysis` as a small function with no `chdir`,
plot display, or file write at import time.

## Compatibility

Existing notebooks can continue using `from helper_functions import ...`.
The compatibility functions now return their result (for example, figures,
fit results, or output paths), making them easier to compose and test.
