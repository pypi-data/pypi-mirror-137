from collections import OrderedDict
from numba.experimental import jitclass
from numba import float64, int64
import numpy as np


solver_spec = OrderedDict()
solver_spec['domX'] = float64     # dimensionless domain length in x
solver_spec['domY'] = float64     # dimensionless domain length in y
solver_spec['minN_log2'] = int64  # log2 minimum number of Chebyshev points
solver_spec['minN'] = int64       # minimum number of Chebyshev points
solver_spec['maxN_log2'] = int64  # log2 maximum number of Chebyshev points
solver_spec['maxN'] = int64       # maximum number of Chebyshev points
solver_spec['Nx_log2'] = int64    # log2 of number of points in x
solver_spec['Nx'] = int64         # number of points in x
solver_spec['Ny_log2'] = int64    # log2 of number of points in y
solver_spec['Ny'] = int64         # number of points in y
solver_spec['chebIts'] = int64    # number of chebyshev iterates
solver_spec['epsilon'] = float64  # tolerance for converged spectral series
solver_spec['meps'] = float64     # Machine epsilon


@jitclass(solver_spec)
class SolverParameters():
    def __init__(self, domX=1.5, domY=1.5, minN_log2=4, maxN_log2=8, Nx_log2=8,
                 Ny_log2=8, epsilon=1e-8):
        self.meps = np.finfo(np.float64).eps

        if domX < 0:
            raise ValueError('In SolverParameters, must have domX>0')
        self.domX = np.float64(domX)  # Dimensionless domain size in x

        if domY < 0:
            raise ValueError('In SolverParameters, must have domY>0')
        self.domY = np.float64(domY)  # Dimensionless domain size in y

        if minN_log2 < 0:
            raise ValueError('In SolverParameters, must have minN_log2>0')
        self.minN_log2 = np.int64(minN_log2)  # Minimum z-resolution (log2)
        self.minN = 2**self.minN_log2

        if maxN_log2 < 0:
            raise ValueError('In SolverParameters, must have maxN_log2>0')
        self.maxN_log2 = np.int64(maxN_log2)  # Maximum z-resolution (log2)
        self.maxN = 2**self.maxN_log2

        if minN_log2 > maxN_log2:
            raise ValueError(
                'In SolverParameters, must have minN_log2 < maxN_log2')

        if Nx_log2 < 0:
            raise ValueError('In SolverParameters, must have Nx_log2>0')
        self.Nx_log2 = np.int64(Nx_log2)  # x-resolution (log2)
        self.Nx = 2**self.Nx_log2

        if Ny_log2 < 0:
            raise ValueError('In SolverParameters, must have Ny_log2>0')
        self.Ny_log2 = np.int64(Ny_log2)  # y-resolution (log2)
        self.Ny = 2**self.Ny_log2

        self.chebIts = self.maxN_log2 - self.minN_log2 + 1

        if epsilon < 0:
            raise ValueError('In SolverParameters, must have epsilon>0')
        if epsilon < 10*self.meps:
            raise ValueError(
                'In SolverParameters, '
                + 'must have epsilon >= 10*machine epsilon')
        self.epsilon = np.float64(epsilon)

    def describe(self):
        print("Solver parameters for AshDisperse")
        print("  Dimensionless domain size in x, domX = ", self.domX)
        print("  Dimensionless domain size in y, domY = ", self.domY)
        print("  Minimum resolution in z, minN = ", self.minN,
              " (minN_log2 = ", self.minN_log2, ")")
        print("  Maximum resolution in z, maxN = ", self.maxN,
              " (maxN_log2 = ", self.maxN_log2, ")")
        print("  Number of Chebyshev iterates = ", self.chebIts)
        print("  Tolerance for Chebyshev series, epsilon = ", self.epsilon)
        print("  Resolution in x, Nx = ", self.Nx,
              " (Nx_log2 = ", self.Nx_log2, ")")
        print("  Resolution in y, Ny = ", self.Ny,
              " (Ny_log2 = ", self.Ny_log2, ")")
        print("********************")


# pylint: disable=E1101
SolverParameters_type = SolverParameters.class_type.instance_type
