from collections import OrderedDict
from numba.experimental import jitclass
from numba import float64


met_spec = OrderedDict()
met_spec['U_scale'] = float64      # scale for wind velocity
met_spec['Ws_scale'] = float64[:]  # settling scale for each grain class


@jitclass(met_spec)
class MetParameters():
    def __init__(self, U_scale, Ws_scale):
        self.U_scale = U_scale
        self.Ws_scale = Ws_scale


# pylint: disable=E1101
MetParameters_type = MetParameters.class_type.instance_type
