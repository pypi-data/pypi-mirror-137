from numba import njit, complex128, float64, prange
from numba.types import Tuple
import numpy as np

from ashdisperse.params import Parameters_type

import ashdisperse.spectral.cheb as cheb

from ashdisperse.containers import (ChebContainer_type, VelocityContainer_type)

import ashdisperse.core.core as core


@njit(Tuple((complex128[::1], complex128[:, ::1]))(float64, float64, complex128[::1], ChebContainer_type, Parameters_type, VelocityContainer_type), cache=True, parallel=False, fastmath=True)
def ade_mode_solve(kx, ky, fxy_ij, ChebContainer, parameters,
                   VelocityContainer):

    z = np.zeros((parameters.output.Nz), dtype=np.float64)
    z = parameters.output.altitudes
    z = z/parameters.source.PlumeHeight
    Nlow = z[z <= 1].size

    conc_0_ft = np.zeros((parameters.grains.bins), dtype=np.complex128)
    conc_z_ft = np.zeros((z.size, parameters.grains.bins), dtype=np.complex128)

    for grain_i in range(parameters.grains.bins):
        """Lower domain.
             Solve for:
               inhomogeneous part (called p1) with null boundary conditions
               homogeneous part (called r1) with bcs r1(1) = 1, r1(-1) = 0
               homogeneous part (called l1) with bcs l1(1) = 0, l1(-1) = 1
               with _c for coefficients, _v for values)
        """
        p1_c, l1_c, r1_c = core.LowerODE(kx, ky, fxy_ij[grain_i], np.int64(grain_i),
                                    ChebContainer,
                                    parameters,
                                    VelocityContainer)

        dp1_p1 = cheb.cheb_dif_p1(p1_c)
        dr1_p1 = cheb.cheb_dif_p1(r1_c)
        dl1_p1 = cheb.cheb_dif_p1(l1_c)

        dp1_m1 = cheb.cheb_dif_m1(p1_c)
        dr1_m1 = cheb.cheb_dif_m1(r1_c)
        dl1_m1 = cheb.cheb_dif_m1(l1_c)

        """Upper domain.
             Solve for:
               inhomogeneous part (called p2) with null boundary conditions
               homogeneous part (called r2) with bcs r2(1) = 1, r2(-1) = 0
               with _c for coefficients, _v for values)
        """
        l2_c = core.UpperODE(kx, ky, np.int64(grain_i),
                        ChebContainer,
                        parameters,
                        VelocityContainer)

        dl2_m1 = cheb.cheb_dif_m1(l2_c)

        a = dl1_m1
        b = dr1_m1
        c = dl1_p1
        d = dr1_p1-dl2_m1

        b0 = -dp1_m1
        b1 = -dp1_p1

        delta = a*d-b*c

        match0 = (b0*d - b1*b)/delta
        match1 = (b1*a - b0*c)/delta

        Cheb_r1 = np.zeros((parameters.output.Cheb_lower.shape[0], r1_c.size),
                           dtype=np.complex128)
        Cheb_l1 = np.zeros((parameters.output.Cheb_lower.shape[0], l1_c.size),
                           dtype=np.complex128)
        Cheb_p1 = np.zeros((parameters.output.Cheb_lower.shape[0], p1_c.size),
                           dtype=np.complex128)

        Cheb_r1[:, :r1_c.size] = parameters.output.Cheb_lower[:, :r1_c.size]
        Cheb_l1[:, :l1_c.size] = parameters.output.Cheb_lower[:, :l1_c.size]
        Cheb_p1[:, :p1_c.size] = parameters.output.Cheb_lower[:, :p1_c.size]

        r1_v = Cheb_r1 @ r1_c
        l1_v = Cheb_l1 @ l1_c
        p1_v = Cheb_p1 @ p1_c

        conc_z_ft[:Nlow, grain_i] = p1_v + match0*l1_v + match1*r1_v

        Cheb_l2 = np.zeros((parameters.output.Cheb_upper.shape[0], l2_c.size),
                           dtype=np.complex128)
        Cheb_l2[:, :l2_c.size] = parameters.output.Cheb_upper[:, :l2_c.size]
        l2_v = Cheb_l2 @ l2_c

        conc_z_ft[Nlow:, grain_i] = match1*l2_v

        conc_0_ft[grain_i] = match0  # (b0*d - b1*b)/delta

    return conc_0_ft, conc_z_ft


@njit(Tuple((complex128[:, :, ::1], complex128[:, :, :, ::1]))(float64[::1], float64[::1], complex128[:, :, ::1], ChebContainer_type, Parameters_type, VelocityContainer_type), parallel=True, cache=True, fastmath=True)
def ade_ft_system(kx, ky, fxy_f, cheby, params, velocities):

    Nx = kx.size
    Ny = ky.size

    conc_0_fft = np.zeros((Ny, Nx, params.grains.bins), dtype=np.complex128)
    conc_z_fft = np.zeros((Ny, Nx, params.output.Nz, params.grains.bins),
                          dtype=np.complex128)

    # do kx = ky = 0:
    conc_0_mode_fft, conc_z_mode_fft = ade_mode_solve(0.0, 0.0, fxy_f[0, 0, :],
                                                      cheby, params,
                                                      velocities)
    conc_0_fft[0, 0, :] = conc_0_mode_fft
    conc_z_fft[0, 0, :, :] = conc_z_mode_fft

    # do kx = 0, ky = 1 ... Ny/2-1, -Ny/2
    # and we get kx = 0, ky = -Ny/2+1, ... , -1 for free by conjugation
    for j in prange(1, Ny//2+1):

        conc_0_mode_fft, conc_z_mode_fft = ade_mode_solve(
            0.0, ky[j], fxy_f[j, 0, :], cheby, params, velocities)

        conc_0_fft[j, 0, :] = conc_0_mode_fft
        conc_0_fft[Ny-j, 0, :] = np.conj(conc_0_mode_fft)

        conc_z_fft[j, 0, :, :] = conc_z_mode_fft
        conc_z_fft[Ny-j, 0, :, :] = np.conj(conc_z_mode_fft)

    # do ky = 0, kx = 1 ... Nx/2-1, -Nx/2
    # and we get ky = 0, kx = -Nx/2+1, ... , -1 for free by conjugation
    for i in prange(1, Nx//2+1):

        conc_0_mode_fft, conc_z_mode_fft = ade_mode_solve(
            kx[i], 0.0, fxy_f[0, i, :], cheby, params, velocities)

        conc_0_fft[0, i, :] = conc_0_mode_fft
        conc_0_fft[0, Nx-i, :] = np.conj(conc_0_mode_fft)

        conc_z_fft[0, i, :, :] = conc_z_mode_fft
        conc_z_fft[0, Nx-i, :, :] = np.conj(conc_z_mode_fft)

    # Do first quadrant, kx = 1 ... Nx/2-1, ky = 1 .. Ny/2-1
    # and get the 4th quadrant for free by conjugation.
    # Also do second quadrant, kx = -Nx/2+1 ... -1, ky = 1 .. Ny/2-1
    # and get the third quadrant for free by conjugation.
    for i in prange(1, Nx//2):
        for j in range(1, Ny//2):

            conc_0_mode_fft, conc_z_mode_fft = ade_mode_solve(
                kx[i], ky[j], fxy_f[j, i, :], cheby, params, velocities)
            conc_0_fft[j, i, :] = conc_0_mode_fft
            conc_z_fft[j, i, :, :] = conc_z_mode_fft

            conc_0_mode_fft, conc_z_mode_fft = ade_mode_solve(
                kx[Nx-i], ky[j], fxy_f[j, Nx-i, :],
                cheby, params, velocities)
            conc_0_fft[j, Nx-i, :] = conc_0_mode_fft
            conc_z_fft[j, Nx-i, :, :] = conc_z_mode_fft

            conc_0_fft[Ny-j, Nx-i, :] = np.conj(conc_0_fft[j, i, :])
            conc_0_fft[Ny-j, i, :] = np.conj(conc_0_fft[j, Nx-i, :])

            conc_z_fft[Ny-j, Nx-i, :, :] = np.conj(conc_z_fft[j, i, :, :])
            conc_z_fft[Ny-j, i, :, :] = np.conj(conc_z_fft[j, Nx-i, :, :])

    return conc_0_fft, conc_z_fft
