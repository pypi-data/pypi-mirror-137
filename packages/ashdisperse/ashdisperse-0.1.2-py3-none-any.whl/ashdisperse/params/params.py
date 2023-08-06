import os
import datetime
from collections import OrderedDict
from numba.experimental import jitclass
from numba import optional
import numpy as np

from .solver_params import (SolverParameters, SolverParameters_type)
from .grain_params import (GrainParameters, GrainParameters_type)
from .source_params import (SourceParameters, SourceParameters_type)
from .physical_params import (PhysicalParameters, PhysicalParameters_type)
from .met_params import (MetParameters, MetParameters_type)
from .model_params import (ModelParameters, ModelParameters_type)
from .output_params import (OutputParameters, OutputParameters_type)

from ..queryreport import is_valid_lat
from ..queryreport import is_valid_lon

from ..utilities import latlon_point_to_utm_code


param_spec = OrderedDict()
param_spec['solver'] = optional(SolverParameters_type)
param_spec['grains'] = optional(GrainParameters_type)
param_spec['source'] = optional(SourceParameters_type)
param_spec['physical'] = optional(PhysicalParameters_type)
param_spec['met'] = optional(MetParameters_type)
param_spec['model'] = optional(ModelParameters_type)
param_spec['output'] = optional(OutputParameters_type)


@jitclass(param_spec)
class Parameters():
    def __init__(self):
        self.solver = None
        self.grains = None
        self.source = None
        self.physical = None
        self.met = None
        self.model = None
        self.output = None

    def describe(self):
        print("AshDisperse parameters")
        self.source.describe()
        self.grains.describe()
        self.solver.describe()
        self.physical.describe()
        # self.met.describe()
        self.model.describe()
        self.output.describe()


# pylint: disable=E1101
Parameters_type = Parameters.class_type.instance_type


def copy_parameters(A):
    new_A = Parameters()
    new_A.solver = SolverParameters(
        domX=A.solver.domX,
        domY=A.solver.domY,
        minN_log2=A.solver.minN_log2,
        maxN_log2=A.solver.maxN_log2,
        epsilon=A.solver.epsilon,
        Nx_log2=A.solver.Nx_log2,
        Ny_log2=A.solver.Ny_log2)
    new_A.grains = GrainParameters()
    for j in range(A.grains.bins):
        new_A.grains.add_grain(A.grains.diameter[j],
                               A.grains.density[j],
                               A.grains.proportion[j])
    new_A.source = SourceParameters(
        A.source.latitude,
        A.source.longitude,
        A.source.utmcode,
        A.source.radius,
        A.source.PlumeHeight,
        A.source.MER,
        A.source.duration,
        A.source.Suzuki_k,
        None)
    new_A.physical = PhysicalParameters(
        A.physical.Kappa_h,
        A.physical.Kappa_v,
        A.physical.g,
        A.physical.mu)
    new_A.met = MetParameters(A.met.U_scale, A.met.Ws_scale)
    new_A.model = ModelParameters()
    new_A.model.from_values(
        A.model.SettlingScale,
        A.model.Velocity_ratio,
        A.model.xyScale,
        A.model.Lx,
        A.model.Ly,
        A.model.cScale,
        A.model.QScale,
        A.model.Peclet_number,
        A.model.Diffusion_ratio,
        A.model.sigma_hat,
        A.model.sigma_hat_scale)
    new_A.output = OutputParameters(
        A.output.start,
        A.output.stop,
        A.output.step)
    new_A.output.set_altitudes()
    new_A.output.ChebMats(A.solver.maxN, A.source.PlumeHeight)
    return new_A


def update_parameters(A, met,
                      domX=None,
                      domY=None,
                      minN_log2=None,
                      maxN_log2=None,
                      epsilon=None,
                      Nx_log2=None,
                      Ny_log2=None,
                      grains=None,
                      latitude=None,
                      longitude=None,
                      radius=None,
                      PlumeHeight=None,
                      MER=None,
                      duration=None,
                      Suzuki_k=None,
                      Suzuki_peak=None,
                      Kappa_h=None,
                      Kappa_v=None,
                      g=None,
                      mu=None,
                      U_scale=None,
                      Ws_scale=None,
                      start=None,
                      stop=None,
                      step=None):

    # solver
    if domX is not None:
        A.solver.domX = domX
    if domY is not None:
        A.solver.domY = domY
    if minN_log2 is not None:
        A.solver.minN_log2 = minN_log2
        A.solver.minN = 2**minN_log2
    if maxN_log2 is not None:
        A.solver.maxN_log2 = maxN_log2
        A.solver.maxN = 2**maxN_log2
    A.solver.chebIts = A.solver.maxN_log2-A.solver.minN_log2 + 1
    if epsilon is not None:
        A.solver.epsilon = epsilon
    if Nx_log2 is not None:
        A.solver.Nx_log2 = Nx_log2
        A.solver.Nx = 2**Nx_log2
    if Ny_log2 is not None:
        A.solver.Ny_log2 = Ny_log2
        A.solver.Ny = 2**Ny_log2

    # grains
    if grains is not None:
        if not isinstance(grains, list):
            raise ValueError(
                "in update_parameters, grains must be a list of dicts; "
                + "received {}".format(grains))
        if not all('class' in g and 'diameter' in g
                   and 'density' in g and 'proportion' in g for g in grains):
            raise ValueError(
                "in update parameters, grains must be a list of dicts with "
                + "dict containing the keys 'class', 'diameter', 'density',"
                + " 'proportion'; received {}".format(grains))
        grains = sorted(grains, key=lambda p: p['proportion'], reverse=True)
        for grain in grains:
            grain_i = grain['class'] - 1
            Diameter = grain['diameter']
            Density = grain['density']
            proportion = grain['proportion']
            if grain_i < A.grains.bins:
                if proportion > 0:
                    A.grains.diameter[grain_i] = Diameter
                    A.grains.density[grain_i] = Density
                    A.grains.proportion[grain_i] = proportion
                else:
                    A.grains.remove_grain(grain_i)
            else:
                A.grains.add_grain(Diameter, Density, proportion)
        A.grains.validate()

    # source
    if latitude is not None:
        if is_valid_lat(latitude):
            A.source.latitude = np.float64(latitude)
        else:
            raise ValueError(
                "In update_parameters, latitude must be a valid latitude in "
                + " decimal degrees")
    if longitude is not None:
        if is_valid_lon(longitude):
            A.source.longitude = np.float64(longitude)
        else:
            raise ValueError(
                "In update_parameters, latitude must be a valid longitude in "
                + " decimal degrees")
    if ((latitude is not None) or (longitude is not None)):
        A.source.utmcode = latlon_point_to_utm_code(A.source.latitude,
                                                    A.source.longitude)

    if radius is not None:
        if radius < 0:
            raise ValueError('In update_parameters, radius must be positive')
        A.source.radius = np.float64(radius)

    if PlumeHeight is not None:
        if PlumeHeight < 0:
            raise ValueError(
                "In update_parameters, PlumeHeight must be positive")
        A.source.PlumeHeight = np.float64(PlumeHeight)

    if MER is not None:
        if MER < 0:
            raise ValueError('In update_parameters, MER must be positive')
        A.source.MER = np.float64(MER)

    if duration is not None:
        if duration < 0:
            raise ValueError('In update_parameters, duration must be positive')
        A.source.duration = np.float64(duration)

    if Suzuki_k is not None:
        if Suzuki_k < 1:
            raise ValueError('In update_parameters, must have Suzuki_k>=1')
        A.source.Suzuki_k = np.float64(Suzuki_k)
        A.source.peak_from_k()

    if Suzuki_peak is not None:
        if Suzuki_peak < 0 or Suzuki_peak > 1:
            raise ValueError(
                'In update_parameters, must have 0<Suzuki_peak<=1')
        A.source.Suzuki_peak = Suzuki_peak
        A.source.k_from_peak()

    # physical
    if Kappa_h is not None:
        if Kappa_h < 0:
            raise ValueError(
                'In PhysicalParameters, Kappa_h must be positive')
        A.physical.Kappa_h = np.float64(Kappa_h)

    if Kappa_v is not None:
        if Kappa_v < 0:
            raise ValueError(
                'In PhysicalParameters, Kappa_v must be positive')
        A.physical.Kappa_v = np.float64(Kappa_v)

    if g is not None:
        if g <= 0:
            raise ValueError('In PhysicalParameters, g must be positive')
        A.physical.g = np.float64(g)

    if mu is not None:
        if mu <= 0:
            raise ValueError('In PhysicalParameters, mu must be positive')
        A.physical.mu = np.float64(mu)

    wind_speed = met.max_wind_speed(A.source.PlumeHeight)
    ws = met.settling_speed(A, np.atleast_1d(0.0))[0]
    A.met = MetParameters(wind_speed, ws)

    A.model.from_params(A.solver, A.met, A.source, A.grains, A.physical)

    if start is not None:
        A.output.start = np.float64(start)
    if stop is not None:
        A.output.stop = np.float(stop)
    if step is not None:
        A.output.step = np.float(step)

    A.output.set_altitudes()
    A.output.ChebMats(A.solver.maxN, A.source.PlumeHeight)

    return A


def save_parameters(params, file='parameters.txt'):
    if os.path.exists(file):
        print('WARNING: {outname} already exists and will be replaced'
              .format(outname=file))

    with open(file, 'w') as f:
        f.write('AshDisperse parameters {}\n\n'
                .format(datetime.datetime.now().strftime("%c")))
        # source
        f.write('Source parameters\n')
        f.write('Name = {}\n'.format(params.source.name))
        f.write('Latitude = {}\n'.format(params.source.latitude))
        f.write('Longitude = {}\n'.format(params.source.longitude))
        f.write('UTM code = {}\n'.format(params.source.utmcode))
        f.write('Radius = {}\n'.format(params.source.radius))
        f.write('Plume height = {}\n'.format(params.source.PlumeHeight))
        f.write('Mass eruption rate = {}\n'.format(params.source.MER))
        f.write('Duration = {}\n'.format(params.source.duration))
        f.write('Suzuki k = {}\n'.format(params.source.Suzuki_k))
        f.write('Suzuki peak = {}\n'.format(params.source.Suzuki_peak))
        f.write('\n')

        # grains
        f.write('Grain parameters\n')
        f.write('Grain classes = {}\n'.format(params.grains.bins))
        for j in range(params.grains.bins):
            f.write('Grain {i}:(diameter={d},density={rho},proportion={p})\n'
                    .format(i=j+1, d=params.grains.diameter[j],
                            rho=params.grains.density[j],
                            p=params.grains.proportion[j]))
        f.write('\n')

        # solver
        f.write('Solver parameters\n')
        f.write('domX = {}\n'.format(params.solver.domX))
        f.write('domY = {}\n'.format(params.solver.domY))
        f.write('minN_log2 = {}\n'.format(params.solver.minN_log2))
        f.write('maxN_log2 = {}\n'.format(params.solver.maxN_log2))
        f.write('Nx_log2 = {}\n'.format(params.solver.Nx_log2))
        f.write('Nx = {}\n'.format(params.solver.Nx))
        f.write('Ny_log2 = {}\n'.format(params.solver.Ny_log2))
        f.write('Ny = {}\n'.format(params.solver.Ny))
        f.write('epsilon = {}\n'.format(params.solver.epsilon))
        f.write('\n')

        # physical
        f.write('Physical parameters\n')
        f.write('Kappa_h = {}\n'.format(params.physical.Kappa_h))
        f.write('Kappa_v = {}\n'.format(params.physical.Kappa_v))
        f.write('g = {}\n'.format(params.physical.g))
        f.write('mu = {}\n'.format(params.physical.mu))
        f.write('\n')

        # output
        f.write('Output parameters\n')
        f.write('Lower altitude = {}\n'.format(params.output.start))
        f.write('Upper altitude = {}\n'.format(params.output.stop))
        f.write('Altitude step = {}\n'.format(params.output.step))
        f.write('\n')
    return


def load_parameters(file):
    if not os.path.exists(file):
        raise IOError('AshDisperse parameters file {} not found'.format(file))

    paramslist = open(file, 'r').readlines()
    pdict = dict()
    grainlist = []
    for param in paramslist:
        param = param.rstrip('\n')
        grainval = param.split(':', 2)
        if len(grainval) == 2:
            grainnum = grainval[0].split('Grain')[1].strip(' ')
            grainprops = grainval[1].strip('()').split(',', 3)
            graindict = dict()
            for gp in grainprops:
                (prop, val) = gp.split('=', 2)
                graindict[prop.strip(' ')] = np.float64(val)
            grainlist.append(graindict)

        keyval = param.split('=', 2)
        if len(keyval) == 2:
            key = keyval[0].strip()
            value = keyval[1].strip()
            try:
                pdict[key] = np.float64(value)
            except:
                pdict[key] = value

    params = Parameters()
    params.solver = SolverParameters(domX=pdict['domX'],
                                     domY=pdict['domY'],
                                     minN_log2=pdict['minN_log2'],
                                     maxN_log2=pdict['maxN_log2'],
                                     epsilon=pdict['epsilon'],
                                     Nx_log2=pdict['Nx_log2'],
                                     Ny_log2=pdict['Ny_log2'])

    params.grains = GrainParameters()
    for j in range(int(pdict['Grain classes'])):
        params.grains.add_grain(grainlist[j]['diameter'],
                                grainlist[j]['density'],
                                grainlist[j]['proportion'])

    if 'Name' in pdict:
        Name = pdict['Name']
    else:
        Name = None
    if 'Suzuki k' in pdict:
        Suzuki_k = pdict['Suzuki k']
        Suzuki_peak = None
    elif 'Suzuki peak' in pdict:
        Suzuki_k = None
        Suzuki_peak = pdict['Suzuki peak']
    else:
        raise RuntimeError(
            "Suzuki parameters not set in {}; ".format(file)
            + "need either 'Suzuki k' or 'Suzuki peak' specified")
    params.source = SourceParameters(pdict['Latitude'],
                                     pdict['Longitude'],
                                     pdict['UTM code'],
                                     radius=pdict['Radius'],
                                     PlumeHeight=pdict['Plume height'],
                                     MER=pdict['Mass eruption rate'],
                                     duration=pdict['Duration'],
                                     Suzuki_k=Suzuki_k,
                                     Suzuki_peak=Suzuki_peak,
                                     name=Name)

    params.physical = PhysicalParameters(Kappa_h=pdict['Kappa_h'],
                                         Kappa_v=pdict['Kappa_v'],
                                         g=pdict['g'],
                                         mu=pdict['mu'])

    params.output = OutputParameters(start=pdict['Lower altitude'],
                                     stop=pdict['Upper altitude'],
                                     step=pdict['Altitude step'])
    params.output.set_altitudes()
    params.output.ChebMats(params.solver.maxN, params.source.PlumeHeight)

    # windSpeed = met.max_wind_speed(params.source.PlumeHeight)
    # ws = met.settling_speed(params, np.atleast_1d(0.0))[0]
    # params.met = MetParameters(windSpeed, ws)

    # params.model = ModelParameters()
    # params.model.from_params(params.solver,
    #                          params.met,
    #                          params.source,
    #                          params.grains,
    #                          params.physical)

    return params
