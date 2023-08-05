#!/usr/bin/env python3
"""
This module produces a simulated cone
It is a rotational symmetric structure where the radius along the y-axis is simply a linear function
"""
import numpy as np

import fp23dpy
from .. import simulation

name = "cone"
max_rmse = 0.02  # expected rmse below this value for reconstruction

# Parameters for cone
_cone_rb = 20  # the minimum radius
_cone_ra = -(512 / 2 - _cone_rb) / 512  # the coefficient for how the radius increase


def radius(Y):
    return _cone_ra * Y + _cone_rb  # estimate radius of cone at Y location


shape = (512, 512)


def get_scale(shape):
    return np.min(shape) / 512


def get_mid_y():
    return 20


def get_calibration(shape=shape):
    calibration = fp23dpy.Calibration()
    calibration["T"] = 12.0
    calibration["gamma"] = 0.0
    calibration["theta"] = 15 * np.pi / 180
    calibration["scale"] = get_scale(shape)

    mid_y, mid_x = [get_mid_y(), int(shape[1] / 2)]
    calibration["principal_point"] = [mid_x, mid_y]

    absolute_threeD = simulation.get_rotsym_depth(0, -mid_y, radius).data[0]
    new_x, new_y, absolute_threeD = simulation.get_rotsym_projection_map(
        np.array([0, -mid_y, absolute_threeD]), calibration
    ).data

    calibration["absolute_threeD"] = [int(mid_x), int(mid_y), absolute_threeD]
    return calibration


def get_projected_coordinate_grid(shape=shape, calibration=None):
    scale = get_scale(shape)
    if calibration is None:
        calibration = get_calibration(shape)
    return simulation.get_rotsym_projection_map(
        radius, calibration, shape=shape, scale=scale
    )


def render(shape=shape, calibration=None):
    """Helper function to render the cone structure"""
    if calibration is None:
        calibration = get_calibration(shape)
    coordinate_grid = simulation.get_rotsym_coordinate_grid(
        radius, shape, scale=calibration["scale"], mid_y=get_mid_y()
    )
    return simulation.render(coordinate_grid, shape, calibration, True)
