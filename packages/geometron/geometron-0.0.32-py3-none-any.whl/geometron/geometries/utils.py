import numpy as np
from numpy import ndarray


def plane_normal(points):
    """Returns the normal vector of a plane defined by three non co-linear 3D points
    Parameters
    ----------
    points : tuple or list or numpy.array
        an array-like object of the coordinates of three 3D points
    Returns
    -------
    numpy.array
        the vector normal to the plane
    Examples
    --------
    This example shows how to search for the normal vector of the Oxy plane (assuming first second and thrid components
    of the vectors correspond to components along x, y and z respectively in a cartesian system :
    >>> import numpy as np
    >>> import geometron.geometries.utils as ggu
    >>> a = np.array((0., 0., 0.))
    >>> b = np.array((1., 0., 0.))
    >>> c = np.array((0., 1., 0.))
    >>> ggu.plane_normal([a, b, c])
    array([0., 0., 1.])
    The answer is obviously a unit vector along the z-axis.
    """
    a, b, c = points
    n = np.cross(b - a, c - a)
    n = n / np.linalg.norm(n)
    return n
