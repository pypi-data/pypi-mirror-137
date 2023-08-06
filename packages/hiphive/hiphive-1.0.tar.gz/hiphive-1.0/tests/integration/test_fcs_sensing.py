import numpy as np

from ase.build import bulk
from hiphive import ClusterSpace, ForceConstantPotential
from hiphive.utilities import extract_parameters


def test_fcs_sensing():
    tol = 1e-12

    cutoffs = [5.0, 4.0]
    prim = bulk('Al', a=4.05)
    dim = 4

    ideal = prim.repeat(dim)

    cs = ClusterSpace(prim, cutoffs)
    parameters = np.random.random(cs.n_dofs)
    fcp = ForceConstantPotential(cs, parameters)
    fcs = fcp.get_force_constants(ideal)
    fitted_parameters = extract_parameters(fcs, cs)

    assert np.linalg.norm(fitted_parameters - parameters) < tol
