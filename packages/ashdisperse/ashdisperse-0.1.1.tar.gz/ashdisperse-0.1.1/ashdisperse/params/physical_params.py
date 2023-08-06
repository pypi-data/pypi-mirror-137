from collections import OrderedDict
from numba.experimental import jitclass
from numba import float64
import numpy as np


phys_spec = OrderedDict()
phys_spec['Kappa_h'] = float64  # Horizontal diffusion coefficient
phys_spec['Kappa_v'] = float64  # Vertical diffusion coefficient
phys_spec['g'] = float64        # Gravitational acceleration
phys_spec['mu'] = float64       # Viscosity of air


@jitclass(phys_spec)
class PhysicalParameters():

    def __init__(self, Kappa_h=100, Kappa_v=10, g=9.81, mu=18.5e-6):

        if Kappa_h < 0:
            raise ValueError(
                'In PhysicalParameters, Kappa_h must be positive')
        self.Kappa_h = np.float64(Kappa_h)

        if Kappa_v < 0:
            raise ValueError(
                'In PhysicalParameters, Kappa_v must be positive')
        self.Kappa_v = np.float64(Kappa_v)

        if g <= 0:
            raise ValueError('In PhysicalParameters, g must be positive')
        self.g = np.float64(g)

        if mu <= 0:
            raise ValueError('In PhysicalParameters, mu must be positive')
        self.mu = np.float64(mu)

    def describe(self):
        print("Physical parameters for AshDisperse")
        print("  Horizontal diffusion coefficient Kappa_h = ",
              self.Kappa_h, " m^2/s")
        print("  Vertical diffusion coefficient Kappa_v = ",
              self.Kappa_v, " m^2/s")
        print("  Gravitational acceleration g = ",
              self.g, " m/s^2")
        print("  Viscosity of air mu = ",
              self.mu, " kg/m/s")
        print("********************")


# pylint: disable=E1101
PhysicalParameters_type = PhysicalParameters.class_type.instance_type
