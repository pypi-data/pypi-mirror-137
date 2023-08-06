from collections import OrderedDict
from numba.experimental import jitclass
from numba import float64, int64, optional
from numba.types import unicode_type
import numpy as np

source_spec = OrderedDict()
source_spec['name'] = optional(unicode_type)    # name of source
source_spec['latitude'] = float64               # latitude of source
source_spec['longitude'] = float64              # longitude of source
source_spec['utmcode'] = int64                  # EPSG utm code of source
source_spec['radius'] = float64                 # radius of the source
source_spec['PlumeHeight'] = float64            # height of the source plume
source_spec['MER'] = float64                    # mass eruption rate
source_spec['duration'] = float64               # duration of eruption
source_spec['Suzuki_k'] = optional(float64)     # Suzuki k parameter
source_spec['Suzuki_peak'] = optional(float64)  # Suzuki_peak parameter


@jitclass(source_spec)
class SourceParameters():

    def __init__(self, lat, lon, utmcode,
                 radius=10e3,
                 PlumeHeight=10e3,
                 MER=1e6,
                 duration=18000,
                 Suzuki_k=None,
                 Suzuki_peak=0.9,
                 name=None):


        self.latitude = np.float64(lat)
        self.longitude = np.float64(lon)
        self.utmcode = utmcode

        if radius < 0:
            raise ValueError('In SourceParameters, radius must be positive')
        self.radius = np.float64(radius)

        if PlumeHeight < 0:
            raise ValueError(
                'In SourceParameters, PlumeHeight must be positive')
        self.PlumeHeight = np.float64(PlumeHeight)

        if MER < 0:
            raise ValueError('In SourceParameters, MER must be positive')
        self.MER = np.float64(MER)

        if duration < 0:
            raise ValueError('In SourceParameters, duration must be positive')
        self.duration = np.float64(duration)

        if Suzuki_k is not None:
            if Suzuki_k < 1:
                raise ValueError('In SourceParameters, must have Suzuki_k>=1')
            self.Suzuki_k = np.float64(Suzuki_k)
            self.peak_from_k()

        if Suzuki_peak is not None:
            if Suzuki_peak < 0 or Suzuki_peak > 1:
                raise ValueError(
                    'In SourceParameters, must have 0<Suzuki_peak<=1')
            self.Suzuki_peak = Suzuki_peak
            self.k_from_peak()
        
        if name is not None:
            self.name = name

    def k_from_peak(self):
        self.Suzuki_k = 1./(1.-self.Suzuki_peak)

    def peak_from_k(self):
        self.Suzuki_peak = 1. - 1./self.Suzuki_k

    def describe(self):
        print("Source parameters for AshDisperse")
        print("  Mass eruption rate MER = ", self.MER, " kg/s")
        print("  Eruption duration = ", self.duration, " s")
        print("  Plume height H = ", self.PlumeHeight, " m")
        print("  Gaussian source radius = ", self.radius, " m")
        print("  Suzuki emission profile k-parameter = ", self.Suzuki_k)
        print("  Suzuki emission profile peak-parameter = ", self.Suzuki_peak)
        print("********************")


# pylint: disable=E1101
SourceParameters_type = SourceParameters.class_type.instance_type
