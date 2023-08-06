import numpy as np
from shapely.geometry import Point
from .transforms import rotate_around_vector

ux = np.array([1., 0., 0.])
uy = np.array([0., 1., 0.])
uz = np.array([0., 0., 1.])
null = np.array([0., 0., 0.])


def plane_normal(args):
    """ Returns the normal vector of a plane defined by two non co-linear vectors or three non co-linear 3D points

    Parameters
    ----------
    args : tuple or list or numpy.array
        an array-like object of the coordinates of two 3D vectors or three points 3D points

    Returns
    -------
    numpy.array
        the unit vector normal to the plane

    Examples
    --------
    >>> # This example shows how to search for the normal vector of the Oxy plane from two non co-linear vectors (assuming
    >>> # first, second and thrid components of the vectors correspond to components along x, y and z respectively in a
    >>> # cartesian system) :
    >>> from shapely.geometry import Point
    >>> import geometron.geometries.vectors as ggv
    >>> v1 = Point((1., 0., 0.))
    >>> v2 = Point((0., 1., 0.))
    >>> ggv.plane_normal([v1, v2])
    array([0., 0., 1.])
    The answer is obviously a unit vector along the z-axis.

    >>> # This example shows how to search for the normal vector of the Oxy plane (assuming first, second and thrid components
    >>> # of the vectors correspond to components along x, y and z respectively in a cartesian system) :
    >>> import numpy as np
    >>> import geometron.geometries.vectors as ggv
    >>> p1 = np.array((0., 0., 0.))
    >>> p2 = np.array((1., 0., 0.))
    >>> p3 = np.array((0., 1., 0.))
    >>> ggv.plane_normal([p1, p2, p3])
    array([0., 0., 1.])
    The answer is obviously a unit vector along the z-axis.

    >>> # This example shows how to search for the normal vector of the Oxy plane from three shapely Points (assuming first,
    >>> # second and thrid components of the vectors correspond to components along x, y and z respectively in a cartesian
    >>> # system) :
    >>> from shapely.geometry import Point
    >>> import geometron.geometries.vectors as ggv
    >>> p1 = Point((0., 0., 0.))
    >>> p2 = Point((1., 0., 0.))
    >>> p3 = Point((0., 1., 0.))
    >>> ggv.plane_normal([a, b, c])
    array([0., 0., 1.])
    The answer is obviously a unit vector along the z-axis.
    """

    n_args = len(args)
    if n_args == 2:  # two vectors
        a = np.array([0, 0, 0])
        b, c = args
    elif n_args == 3:  # three points
        a, b, c = args
    else:
        print('Error: Invalid number of arguments.')
        return np.nan

    if isinstance(a, Point):
        a = np.array(a.coords)
    if isinstance(b, Point):
        b = np.array(b.coords)
    if isinstance(c, Point):
        c = np.array(c.coords)

    n = np.cross(b - a, c - a)
    n = n / np.linalg.norm(n)
    return n


def unit_vector(vector):
    """ Computes a unit vector in the direction of the given vector

    Parameters
    ----------
    vector: numpy.array
        the input vector

    Returns
    -------
    numpy.array
        the unit vector in the direction of the input vector

    Examples
    --------
    >>> # This examples shows how to retrieve the unit vector in the direction of vector [1,2,3]
    >>> import numpy as np
    >>> from geometron.geometries import vectors as ggv
    >>> v = np.array([1,2,3])
    >>> ggv.unit_vector(v)
    array([0.26726124, 0.53452248, 0.80178373])
    """

    return vector / np.linalg.norm(vector)


def angle_between_vectors(v1, v2, degrees=False):
    """ Returns the angle between 2 vectors v1 and v2

    if a vector is 2D it is converted to a 3D array with third coordinate set to zero.

    Parameters
    ----------
    v1: numpy.array or list
        first 2D or 3D vector
    v2: numpy.array or list
        second 2D or 3D vector
    degrees: bool, default False
        set to True to return the angle in degrees otherwise the angle is in radians

    Returns
    -------
    float
        angle between v1 and v2

    Examples
    --------
    >>> import numpy as np
    >>> from geometron.geometries import vectors as ggv
    >>> v1 = ggv.ux
    >>> v2 = ggv.uz
    >>> ggv.angle_between_vectors(v1, v2, degrees=True)
    """

    v1 = np.asarray(v1)
    if v1.shape[0] == 2:
        v1 = np.array([v1[0], v1[1], 0.])

    v2 = np.asarray(v2)
    if v2.shape[0] == 2:
        v2 = np.array([v2[0], v2[1], 0.])

    if almost_colinear(v1, v2):
        if np.isclose(np.dot(unit_vector(v1), unit_vector(v2)), 1.0, atol=1e-08):
            angle = 0.
        elif np.isclose(np.dot(unit_vector(v1), unit_vector(v2)), -1.0, atol=1e-08):
            angle = np.pi
        else:
            angle = np.nan
    else:
        angle = np.arctan2(np.dot(np.cross(v1, v2), np.abs(plane_normal([v1, v2]))), np.dot(v1, v2))
    if degrees:
        angle = np.rad2deg(angle)
    return angle


def almost_null(v, atol=1e-08):
    """ Tests if v is almost the null vector (a vector with all coordinates = 0.).

    Parameters
    ----------
    v: numpy.array or list
        input vector
    atol: float, defaut 1e-08
        absolute tolerance used to compare v with null

    Returns
    -------
    bool
        True if v is almost close to null


    Examples
    --------
    >>> import numpy as np
    >>> from geometron.geometries import vectors as ggv
    >>> ggv.almost_null(np.array([0., 0., 0.]))
    True
    """

    return np.allclose(np.asarray(v), null, rtol=0, atol=atol)


def almost_colinear(v1, v2, atol=1e-08):
    """ Tests if vectors v1 and v2 are almost colinear.

    Parameters
    ----------
    v1: numpy.array or list
        first 2D or 3D vector
    v2: numpy.array or list
        second 2D or 3D vector
    atol: float, default 1e-08
        absolute tolerance used to compare the norm of the cross product between v1 and v2 with zero

    Returns
    -------
    bool
        True if v1 and v2 are almost colinear

    Examples
    --------
    >>> # This example shows that ux is colinear with the cross product of uy by uz
    >>> import numpy as np
    >>> from geometron.geometries import vectors as ggv
    >>> ggv.almost_colinear(ggv.ux, np.cross(ggv.uy, ggv.uz))
    True
    """

    v1 = np.asarray(v1)
    if v1.shape[0] == 2:
        v1 = np.array([v1[0], v1[1], 0.])

    v2 = np.asarray(v2)
    if v2.shape[0] == 2:
        v2 = np.array([v2[0], v2[1], 0.])

    norm = np.linalg.norm(np.cross(v1, v2))
    return np.isclose(norm, 0.0, rtol=0, atol=atol)


def dip_and_strike_vectors(dip, strike, degrees=False):
    """ Computes the unit vectors along the dip and the strike directions

    Parameters
    ----------
    dip: float
        dip angle counted using the right-hand side rule
    strike: float
        strike angle counted clockwise from the North
    degrees: bool, default False
        if True, the angles are given in degrees otherwise in radians

    Returns
    -------
    numpy.array
        unit vectors along the dip and the strike directions

    Examples
    --------
    >>> # This example shows how to retrieve the unit vectors along the dip and the strike directions N120°E 60°S
    >>> import numpy as np
    >>> from geometron.geometries import vectors as ggv
    >>> ggv.dip_and_strike_vectors(60., 120., degrees=True)
    (array([-0.25     , -0.4330127, -0.8660254]),
    array([ 0.8660254, -0.5      ,  0.       ]))
    """

    if degrees:
        dip, strike = np.deg2rad([dip, strike])

    strike_vector = np.array([0., 1., 0.])
    dip_vector = np.array([1., 0., 0.])

    rotation = rotate_around_vector(uz, -strike)
    strike_vector = np.dot(rotation, strike_vector)
    dip_vector = np.dot(rotation, dip_vector)
    rotation = rotate_around_vector(strike_vector, dip)
    dip_vector = np.dot(rotation, dip_vector)
    return dip_vector, strike_vector


def plane_normal_from_dip_and_strike(dip, strike, degrees=False):
    """ Computes the unit vector normal to the plane defined by the dip and the strike directions

    Parameters
    ----------
    dip: float
        dip angle counted using the right-hand side rule
    strike: float
        strike angle counted clockwise from the North
    degrees: bool, default False
        if True, the angles are given in degrees otherwise in radians

    Returns
    -------
    numpy.array
        unit vector normal to the plane defined by dip and strike

    Examples
    --------
    >>> # This example shows how to retrieve the unit vector along the normal of the plane defined by dip and the strike
    >>> # directions N120°E 60°S
    >>> import numpy as np
    >>> from geometron.geometries import vectors as ggv
    >>> ggv.plane_normal_from_dip_and_strike(60., 120., degrees=True)
    array([-0.4330127, -0.75     ,  0.5      ])
    """

    dip_vector, strike_vector = dip_and_strike_vectors(dip, strike, degrees=degrees)
    n = np.cross(dip_vector, strike_vector)
    return unit_vector(n)
