# -*- coding: utf-8 -*-
"""Grain parameters for AshDisperse.

Defines the GrainParameters class, containing attributes specifying grains
classes and methods for amending these, and a printer for this object.

Example:
    grains = GrainParameters()
    grains.add_grains(1e-4,1400,0.5)
    grains.add_grains(1e-3,1400,0.5)

    print_grain_parameters(grains)
"""

from collections import OrderedDict
from numba.experimental import jitclass
from numba import float64, int64
from numba.types import ListType
from numba.typed import List
import numpy as np

grain_spec = OrderedDict()
grain_spec['bins'] = int64                    # Number of grain classes
grain_spec['diameter'] = ListType(float64)    # Grain sizes
grain_spec['density'] = ListType(float64)     # Grain densities
grain_spec['proportion'] = ListType(float64)  # Grain proportions
"""OrderedDict: GrainParameters attribute type specification.

This specification is required for numba jitting.
"""


@jitclass(grain_spec)
class GrainParameters():
    """Grain parameters required for AshDisperse.

    Defines the GrainParameters class, containing attributes specifying grains
    classes and methods for amending these.

    Attributes:
        bins: An integer count of the number of grain classes.
        diameter: A list of floats containing the diameter of each grain class.
        density: A list of floats containing the density of each grain class.
        proportion: A list of floats containing the proportion of each grain
                    class.
    """

    def __init__(self):
        """Initialize of GrainParameters to empty lists.

        Use add_grain to add grains.
        """
        self.bins = 0
        self.diameter = List.empty_list(np.float64)
        self.density = List.empty_list(np.float64)
        self.proportion = List.empty_list(np.float64)

    def add_grain(self, diameter, density, proportion):
        """Add a grain class to the GrainParameters object.

        A grain class requires a diameters, density and proportion.
        The proportions must sum to one.
        Adding a grain increments the number of classes through the bins
        attribute.

        Args:
            diameter: [float64] The diameter of the grain class;
                must be positive.
            density: [float64] The density of the grain class;
                must be positive.
            proportion: [float64] The proportion of the total mass in this
                grain class; must be in the range (0,1].
        """
        if diameter < 0:
            raise ValueError('Grain diameter must be positive')
        if density < 0:
            raise ValueError('Grain density must be positive')
        if proportion < 0:
            raise ValueError('Grain proportion must be in [0,1]')
        if proportion > 1:
            raise ValueError('Grain proportion must be in [0,1]')
        self.diameter.append(np.float64(diameter))
        self.density.append(np.float64(density))
        self.proportion.append(np.float64(proportion))
        self.bins += 1

    def remove_grain(self, grain_i):
        """Remove a grain class to the GrainParameters object.

        The grain class with a given index is removed from the GrainParameters
        object.
        Removing a grain decrements the number of classes through the bins
        attribute.

        Args:
            grain_i: [int] The index of the grain class.  Must be less than the
                           number of grain classes.
        """
        if grain_i < 0:
            raise ValueError('index to grain class must be positive')
        if grain_i >= self.bins:
            raise ValueError(
                'index must in range [0,{}]'.format(self.bins-1))
        self.diameter.pop(grain_i)
        self.density.pop(grain_i)
        self.proportion.pop(grain_i)
        self.bins -= 1

    def validate(self):
        """Validate grain classes in GrainParameters object."""
        retval = 1
        if len(self.diameter) != self.bins:
            print('In GrainParameters: number of grain diameter values (',
                  len(self.diameter), ') must equal number of grain classes (',
                  self.bins, ')')
            retval = 0
        if len(self.density) != self.bins:
            print('In GrainParameters: number of grain density values must '
                  + 'equal number of grain classes')
            retval = 0
        if len(self.proportion) != self.bins:
            print('In GrainParameters: number of grain proportion values '
                  + 'must equal number of grain classes')
            retval = 0
        sum_prop = np.sum(np.array(list(self.proportion),
                                   dtype=float64), dtype=float64)
        if np.abs(sum_prop - 1.0) > np.finfo(np.float64).eps:
            print('In GrainParameters: the sum of the proportions for the '
                  + 'grain classes must be unity')
            retval = 0
        return retval

    def describe(self):
        """Describe the grain classes in GrainParameters object."""
        print("Grain parameters for AshDisperse")
        print("  Number of grain classes, N_grains = ", self.bins)
        for j in range(self.bins):
            print("  Grain class ", j+1)
            print("    Grain diameter = ", self.diameter[j], " m")
            print("    Grain density = ", self.density[j], " kg/m^3")
            print("    proportion = ", self.proportion[j])
        print("********************")


# pylint: disable=E1101
GrainParameters_type = GrainParameters.class_type.instance_type
