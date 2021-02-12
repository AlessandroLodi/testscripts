import kwant
from matplotlib import pyplot
import numpy as np
import numpy.linalg as npl

lat = kwant.lattice.square()
syst = kwant.Builder()
syst[(lat(x, 0) for x in range(20))] = 0  # I think this uses a generator

syst[((lat(x, 0), lat(x + 1, 0)) for x in range(19))] = -1

sym = kwant.TranslationalSymmetry((-1, 0))
lead_1 = kwant.Builder(sym)
lead_1[lat(0, 0)] = 0
lead_1[lat(0, 0), lat(1, 0)] = -1


syst.attach_lead(lead_1)
syst.attach_lead(lead_1.reversed())

# Numeric Solution
fsyst = syst.finalized()
syst_matrix = fsyst.hamiltonian_submatrix()
evs = npl.eigvalsh(syst_matrix)  # compute eigs for an Hermitian Matrix

# Analytical Solution

fsyst = syst.finalized()
Es = np.linspace(-3, 3, 20)
gs = []

for E in Es:
    S = kwant.smatrix(fsyst, E)
    gs.append(S.transmission(1, 0))

pyplot.plot(Es, gs, "ok-")
pyplot.xlabel("$E_F \quad [t]$")
pyplot.ylabel("$g \quad [e^2/h]$")


syst[lat(2, 0)] = 1  # introduce a barrier on this lattice site on the left
syst[lat(14, 0)] = 1  # introduce a barrier on this lattice site on the right

fsyst = syst.finalized()
Es = np.linspace(-3, 3, 20)
gs = []

for E in Es:
    S = kwant.smatrix(fsyst, E)
    gs.append(S.transmission(1, 0))

pyplot.plot(Es, gs, "ok-")
pyplot.xlabel("$E_F \quad [t]$")
pyplot.ylabel("$g \quad [e^2/h]$")
pyplot.title("Fabry-Perot Conductance")
pyplot.show()
pyplot.savefig("fabry_perot_conductance.png", format="png")
