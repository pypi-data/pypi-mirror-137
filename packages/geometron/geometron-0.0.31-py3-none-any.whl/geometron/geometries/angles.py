import numpy as np
# from shapely.geometry import Point


def ddmm_to_dd(x):
    """
    Converts angle expressed as degrees minutes (DDDMM) to decimal degrees (DDD.XXX)

    Parameters
    ----------
    x : float
         angle in degrees minute

    Returns
    -------
    angle : float
            angle converted to the decimal degrees format
    """

    degrees = float(x) // 100
    minutes = x - 100. * degrees
    return degrees + minutes / 60.


def azimuth(origin, target):
    """
    Computes the Azimuth of a target point as seen from a origin point in a planar coordinate system

    Parameters
    ----------
    origin : shapely.geometry.Point
             Point from which the target is observed

    target : shapely.geometry.Point
             Point which is observed from the origin
    Returns
    -------
    azimuth: `float`
             azimuth angle in radians

    """

    az = np.arctan2(target.coords[0][0] - origin.coords[0][0], target.coords[0][1] - origin.coords[0][1])
    az = np.fmod(az + 2 * np.pi, 2 * np.pi)
    return az
