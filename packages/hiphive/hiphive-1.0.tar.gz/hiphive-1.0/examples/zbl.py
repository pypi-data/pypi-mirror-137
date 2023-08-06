from ase.build import bulk
from ase.md.verlet import VelocityVerlet
from ase.md.velocitydistribution import ZeroRotation, Stationary, MaxwellBoltzmannDistribution
from ase import units
from hiphive.calculators.zbl import ZBLCalculator

T = 300
dt = 0.1
size = 3
a = 1.0
cutoff = 3
skin = 1
steps = 10000
traj_name = 'zbl.traj'

atoms = bulk('H', crystalstructure='fcc', a=a, cubic=True).repeat(size)

atoms.calc = ZBLCalculator(cutoff=cutoff, skin=skin)

MaxwellBoltzmannDistribution(atoms, temperature_K=2*T, force_temp=True)
ZeroRotation(atoms)
Stationary(atoms)

dyn = VelocityVerlet(atoms, timestep=0.1*units.fs, logfile='-', trajectory=traj_name)

dyn.run(steps)
