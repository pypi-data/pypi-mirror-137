"""
Prepare training structures for FCC-Ni using an EMT calculator and a
Monte Carlo rattle approach for generating displacements.

Runs in approximately 10 seconds on an Intel Core i5-4670K CPU.
"""

from ase.io import write
from ase.build import bulk
from ase.calculators.emt import EMT
from hiphive.structure_generation import generate_mc_rattled_structures
from hiphive.utilities import prepare_structures


# parameters
structures_fname = 'rattled_structures.extxyz'
n_structures = 5
cell_size = 4
rattle_std = 0.03
minimum_distance = 2.3

# setup
atoms_ideal = bulk('Ni', cubic=True).repeat(cell_size)
calc = EMT()

# generate structures
structures = generate_mc_rattled_structures(atoms_ideal, n_structures, rattle_std, minimum_distance)
structures = prepare_structures(structures, atoms_ideal, calc)

# save structures
write(structures_fname, structures)
