# -*- coding: utf-8 -*-
"""AshDisperse -- a steady-state volcanic ash dispersion model.

AshDisperse implements an efficient and accurate numerical method for solving
the advection-diffusion-sedimentation equation for tephra classes of different
characteristics in a wind field.

Example:
    params, met = setup(gui=False)

    result = solve(params, met, timer=True)

    for grain_i in range(0, params.grains.bins):
        result.plot_settling_flux_for_grain_class(grain_i)
        result.plot_conc_for_grain_class(grain_i)
        result.plot_iso_conc_for_grain_class(grain_i, 1e-4)

    result.plot_ashload(resolution=500., vmin=1e-4, nodata=-1,
                        export_gtiff=True, export_name='AshLoad.tif')
"""
import os

os.environ['OMP_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['VECLIB_MAXIMUM_THREADS'] = '1'
os.environ['NUMEXPR_NUM_THREADS'] = '1'

import time
import numpy as np
from scipy.fft import ifft2

from .interface import set_met, set_parameters
from .containers import ChebContainer, VelocityContainer
from .spectral import grid_freq
from .solver import source_xy_dimless, ade_ft_system
from .core import AshDisperseResult
from .config import set_num_threads, set_default_threads, get_max_threads, get_num_threads
set_default_threads()

def setup(gui=False):
    """Set parameters and meteorological data for AshDisperse.

    The Parameters class object stores the parameters required for the model
    and the MetData class object stores meteorological data.
    setup() instantiates and initializes these objects.

    Args:
        gui (bool, optional): Use a tkinter gui; defaults to False.

    Returns:
        params_set (Parameters): A Parameters object containing parameters.
        met_set (MetData): A MetData object containing meteorological data.
    """
    params_set = set_parameters()
    params_set, met_set = set_met(params_set, gui=gui)
    return params_set, met_set


def solve(parameters, met_data, timer=False):
    """Run the numerical solver using parameters and meteorological data.

    Args:
        parameters (Parameters): A set of parameters contained in a Parameters
                                 object.
        met_data (MetData): Meteorological data contained in a MetData object.
        timer (bool, optional): Run a timer of stages of the solver;
                                defaults to False.

    Returns:
        AshDisperseResult: An AshDisperseResult object containing the model
                           results.
    """
    cheby = ChebContainer(parameters)

    velocities = VelocityContainer(parameters, met_data, cheby.x)

    x, kx = grid_freq(parameters.solver.Nx)
    y, ky = grid_freq(parameters.solver.Ny)

    _, fxy_f = source_xy_dimless(x, y, parameters)
    # fxy,fxy_f = source_xy_dimless_flat(x,y,params)

    res_x = x[1] - x[0]
    res_y = y[1] - y[0]

    if timer:
        start = time.time()
    conc_0_FT = np.zeros((parameters.solver.Ny, parameters.solver.Nx,
                          parameters.grains.bins), dtype=np.complex128)
    conc_z_FT = np.zeros((parameters.solver.Ny, parameters.solver.Nx,
                          parameters.output.Nz, parameters.grains.bins),
                         dtype=np.complex128)
    conc_0_FT, conc_z_FT = ade_ft_system(kx, ky, fxy_f, cheby, parameters,
                                         velocities)
    if timer:
        mid = time.time()
    conc_0 = np.zeros(np.shape(conc_0_FT))
    conc_z = np.zeros(np.shape(conc_z_FT))
    for igrain in range(0, parameters.grains.bins):
        conc_0[:, :, igrain] = (np.real(ifft2(conc_0_FT[:, :, igrain]))
                                / (res_x*res_y))
        for k in range(0, parameters.output.Nz):
            conc_z[:, :, k, igrain] = np.real(
                ifft2(conc_z_FT[:, :, k, igrain]))/(res_x*res_y)
    if timer:
        end = time.time()

    if timer:
        print('Equation solve time : ', mid-start)
        print('Inverse FFT time : ', end-mid)
        print('Total solve time : ', end-start)

    return AshDisperseResult(parameters, velocities, x, y, conc_0, conc_z)


if __name__ == "__main__":

    print("Running AshDisperse")

    params = set_parameters()

    Met, params = set_met(params)

    result = solve(params, Met, timer=True)

    for grain_i in range(0, params.grains.bins):
        result.plot_settling_flux_for_grain_class(grain_i)
        result.plot_conc_for_grain_class(grain_i)
        result.plot_iso_conc_for_grain_class(grain_i, 1e-4)

    _ = result.get_ashload(resolution=500., vmin=1e-4, nodata=-1,
                           export_gtiff=True, export_name='AshLoad.tif')

    result.plot_ashload(resolution=500, vmin=0.1)
