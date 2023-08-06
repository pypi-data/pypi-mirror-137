"""
Construct a ForceConstantPotential from training data generated previously.

Runs in approximately 100 seconds on an Intel Core i5-4670K CPU.
"""

from ase.io import read
from hiphive import ClusterSpace, StructureContainer, ForceConstantPotential
from trainstation import Optimizer

# read structures containing displacements and forces
structures = read('rattled_structures.extxyz@:')

# set up cluster space
cutoffs = [5.0, 4.0, 4.0]
cs = ClusterSpace(structures[0], cutoffs)
print(cs)
cs.print_orbits()

# ... and structure container
sc = StructureContainer(cs)
for structure in structures:
    sc.add_structure(structure)
print(sc)

# train model
opt = Optimizer(sc.get_fit_data())
opt.train()
print(opt)

# construct force constant potential
fcp = ForceConstantPotential(cs, opt.parameters)
fcp.write('fcc-nickel.fcp')
print(fcp)
