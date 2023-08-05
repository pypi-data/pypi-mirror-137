import numpy as np
import scipy
import trimesh

from . import threeD_to_phase_const
from . import export
from . import helpers as h


def _create_camera_matrix(calibration):  # not fully implemented
    if "camera_type" in calibration:
        raise ValueError("camera_type not supported yet")
    else:
        return np.eye((3, 4))


def estimate_projection_map(
    coordinate_grid, calibration, image_shape
):  # currently not fully implemented
    assert len(image_shape) == 2

    n_pixels = np.prod(image_shape)

    mesh = export.mesh_it({"grid": coordinate_grid})
    ray_tracer = trimesh.ray.ray_triangle.RayMeshIntersector(mesh)
    ray_origins = None
    ray_directions = None
    try:
        _, rays, locations = ray_tracer.intersects_id(
            ray_origins, ray_directions, return_locations=True, multiple_hits=False
        )
    except:
        raise EnvironmentError("Install trimesh[easy] for this method to work")
    
    mask = np.ones(n_pixels, dtype=bool)
    Xmap = np.zeros(n_pixels)
    Ymap = np.zeros(n_pixels)
    dmap = np.zeros(n_pixels)

    mask[rays] = True
    Xmap[rays] = locations[:, 0]
    Ymap[rays] = locations[:, 1]
    dmap[rays] = locations[:, 2]

    mask.shape = Xmap.shape = Ymap.shape = dmap.shape = image_shape
    Xmap = np.ma.array(Xmap, mask=mask)
    Ymap = np.ma.array(Ymap, mask=mask)
    dmap = np.ma.array(dmap, mask=mask)
    return np.ma.stack(Xmap, Ymap, dmap)


#### Simplified functions for rotational symmetry in the XZ plane ###
def get_rotsym_depth(X, Y, radius):
    """Get the third coordinate of from X and Y (X and Y must have same shape) coordinates.
    Radius is either a function or value that describes the radius of the rotational symmetric structure in the XZ plane"""
    if isinstance(X, (int, float)):
        X = np.array([X])
        Y = np.array([Y])
    assert X.shape == Y.shape
    cone = np.zeros(X.shape)
    if hasattr(radius, "__call__"):
        # radius is a function that takes the Y parameter
        rs = radius(Y)
    else:
        # assuming radius is a number
        rs = np.ones(X.shape) * radius
    inside = np.abs(X) < rs
    cone[inside] = rs[inside] * np.sin(np.arccos(X[inside] / rs[inside]))
    cone = np.ma.array(cone, mask=~inside)
    return cone


def get_rotsym_coordinate_grid(radius, shape, scale=1, mid_y=0):
    """Create 3D coordinated for a half of the rotational symmetric structure described by radius function or value."""
    mid_x = shape[0] / 2

    Y, X = np.mgrid[: shape[0], : shape[1]]
    X = (X - mid_x) / scale
    Y = -(Y - mid_y) / scale
    depth = get_rotsym_depth(X, Y, radius)
    mask = depth.mask
    return np.ma.stack((np.ma.array(X, mask=mask), np.ma.array(Y, mask=mask), depth))


def get_rotsym_projection_map(coordinate_grid, calibration, **kwargs):
    """Camera mapping of image x to world X coordinate on the cone structure taking advantage of rotational symmetry"""
    if len(kwargs) > 0:
        # Assuming here that the coordinate_grid variable is radius to estimate coordinate_grid
        coordinate_grid = get_rotsym_coordinate_grid(radius=coordinate_grid, **kwargs)
    if not np.ma.isMaskedArray(coordinate_grid):
        coordinate_grid = np.ma.array(coordinate_grid)
    shape = coordinate_grid.shape
    coordinate_grid = coordinate_grid.reshape((3, -1))
    theta = calibration["theta"]
    Xmap = coordinate_grid[0] * np.cos(theta) + coordinate_grid[2] * np.sin(theta)
    proj_cone = -coordinate_grid[0] * np.sin(theta) + coordinate_grid[2] * np.cos(theta)
    masked = proj_cone < 0
    Xmap[masked] = np.ma.masked
    Ymap = np.ma.array(coordinate_grid[1], mask=Xmap.mask)
    proj_cone[masked] = np.ma.masked
    return np.ma.stack((Xmap, Ymap, proj_cone)).reshape(shape)


#################


def render_from_map(dmap, calibration, amplitude=1, background=1):
    """
    Method used to simulate an FP image of a 3D structure by mainly using a map of the world third coordinate of the object surface in the camera.
    Assumes that an orthographic camera rotated theta radians round the y-axis.
    If not the full image is used as for the drop case the dmap parameter should be a masked numpy array and the function will always return a masked array.
    """
    dmap = np.ma.asarray(dmap)
    tpc = threeD_to_phase_const(
        calibration["T"], calibration["theta"], calibration["scale"]
    )
    if "phi" in calibration:
        pass  # multiply constant slightly
    carrier = h.make_carrier(dmap.shape, calibration["T"], calibration["gamma"])
    phase = dmap * tpc + carrier
    signal = amplitude * np.cos(phase) + background

    mask = dmap.mask
    # convolving to simulate the integral over each pixel for a real camera
    kernel = 1 / 5 * np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])
    signal = np.ma.array(scipy.signal.convolve2d(signal, kernel, "same"), mask=mask)
    signal.data[signal.mask] = 0
    return signal


def render(coordinate_grid, shape, calibration, use_rotsym=True):
    """Helper function to render a general 3D structure, if use_rotsym=True rotational symmetry in the XZ plane is assumed."""
    if use_rotsym:
        _, _, dmap = get_rotsym_projection_map(coordinate_grid, calibration)
    else:
        _, _, dmap = estimate_projection_map(coordinate_grid, calibration, shape)
    return render_from_map(dmap, calibration)
