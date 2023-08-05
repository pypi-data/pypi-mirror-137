# Copyright (c) 2019-2021, Jonas Eschle, Jim Pivarski, Eduardo Rodrigues, and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/vector for details.

import typing

"""
.. code-block:: python

    @property
    Spatial.mag2(self)
"""

import numpy

from vector._methods import (
    AzimuthalRhoPhi,
    AzimuthalXY,
    LongitudinalEta,
    LongitudinalTheta,
    LongitudinalZ,
    _aztype,
    _flavor_of,
    _from_signature,
    _ltype,
)


def xy_z(lib, x, y, z):
    return x**2 + y**2 + z**2


def xy_theta(lib, x, y, theta):
    return (x**2 + y**2) / lib.sin(theta) ** 2


def xy_eta(lib, x, y, eta):
    expmeta = lib.exp(-eta)
    invsintheta = 0.5 * (1 + expmeta**2) / expmeta
    return (x**2 + y**2) * invsintheta**2


def rhophi_z(lib, rho, phi, z):
    return rho**2 + z**2


def rhophi_theta(lib, rho, phi, theta):
    return rho**2 / lib.sin(theta) ** 2


def rhophi_eta(lib, rho, phi, eta):
    expmeta = lib.exp(-eta)
    invsintheta = 0.5 * (1 + expmeta**2) / expmeta
    return rho**2 * invsintheta**2


dispatch_map = {
    (AzimuthalXY, LongitudinalZ): (xy_z, float),
    (AzimuthalXY, LongitudinalTheta): (xy_theta, float),
    (AzimuthalXY, LongitudinalEta): (xy_eta, float),
    (AzimuthalRhoPhi, LongitudinalZ): (rhophi_z, float),
    (AzimuthalRhoPhi, LongitudinalTheta): (rhophi_theta, float),
    (AzimuthalRhoPhi, LongitudinalEta): (rhophi_eta, float),
}


def dispatch(v: typing.Any) -> typing.Any:
    function, *returns = _from_signature(
        __name__,
        dispatch_map,
        (
            _aztype(v),
            _ltype(v),
        ),
    )
    with numpy.errstate(all="ignore"):
        return v._wrap_result(
            _flavor_of(v),
            function(v.lib, *v.azimuthal.elements, *v.longitudinal.elements),
            returns,
            1,
        )
