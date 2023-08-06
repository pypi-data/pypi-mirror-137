import numpy as np
from scipy.interpolate import PPoly, PchipInterpolator
from scipy.integrate import quad
from scipy.optimize import root


def cclength(coefs, x_end=1.0):
    """
    Computes the length along a cubic curve defined by the coefficients of its equation z=f(x) from 0 to x_end

    Parameters
    ----------
    coefs: list
           coefficients of the cubic curve

    x_end: float
           length is computed for a portion of the curve whose ends are at x=0 and x=x_end

    Returns
    -------
    length: float
            length the portion of the curve
    """
    # g = lambda x: (1 + (coefs[2] + 2 * coefs[1] * (x) + 3 * coefs[0] * (x) ** 2) ** 2) ** 0.5
    def g(x):
        return (1 + (coefs[2] + 2 * coefs[1] * x + 3 * coefs[0] * x ** 2) ** 2) ** 0.5

    length = quad(g, 0, x_end, epsrel=0.001)

    return length[0]


def cclength2abs(coefs, length):
    """
    Computes the x value of the point at a distance computed along a cubic curve defined by its coefficients

    Parameters
    ----------

    coefs: list
           coefficients of the cubic curve

    length: numpy.array
           length of the portion of the curve

    Returns
    -------
        x: float
           value of the end point of the portion of the curve starting at x=0 and of given length

    """

    def f(x):
        return length - cclength(coefs, x)

    x = root(f, length)
    return x.x


def cclength2xz(known_points, distances):
    """
    Computes [x,z] of points distributed at set distances along a curve defined by a set of known points
    and interpolated as a pchip

    Parameters
    ----------
    known_points: list, numpy.array
        points

    distances: numpy.array
        distances from the origin of the curve to the points whose x_value are sought

    Returns
    -------
    xz: numpy.array
        list of points 2d coordinates in the xz reference system
    """
    if type(known_points) is list:
        known_points = np.array(known_points).T
    sorted_order = np.argsort(distances)
    sorter = np.argsort(sorted_order)
    unsorted_order = sorter[np.searchsorted(sorted_order, np.arange(len(distances)), sorter=np.argsort(sorted_order))]
    distances = np.array(sorted(distances))
    if known_points[0][0] != 0:
        print('Error: The first known point must be at x=0.')
        return -1
    x_i = np.array(known_points[0])
    y_i = np.array(known_points[1])
    interp = PchipInterpolator(x_i, y_i)
    try:
        poly = PPoly.from_bernstein_basis(interp, extrapolate=None)
    except TypeError:
        # already a PPoly instance, nothing to do
        poly = interp
    coefs = poly.c.T
    number_of_points = len(distances)
    number_of_pieces = len(coefs)
    length_of_pieces = []
    for j in range(number_of_pieces):
        length_of_pieces.append(cclength(coefs[j], x_i[j + 1] - x_i[j]))
    i = 0
    j = 0
    xz = np.array([[np.nan, np.nan]] * number_of_points)
    while i < number_of_points:
        if distances[i] <= length_of_pieces[j]:
            xz[i, 0] = x_i[j] + cclength2abs(coefs[j], distances[i])
            xz[i, 1] = interp(xz[i, 0])
            i += 1
        elif j < number_of_pieces - 1:
            distances = distances - length_of_pieces[j]
            j += 1
        else:
            for k in range(i, number_of_points):
                xz[k, 0] = np.nan
                xz[k, 1] = np.nan
            break
    return xz[unsorted_order]


def cclengths(known_points):
    """ computes the distance from the first point and each given point along a curve defined
    by this set of known points and interpolated as a pchip

    Parameters
    ----------
    known_points : list, numpy.array
        2d coordinates of known points used to compute a piecewise cubic curve
    Returns
    -------
    numpy.array
       distances along the curve at each known point
    """
    if type(known_points) is list:
        known_points = np.array(known_points).T
    if known_points[0][0] != 0:
        print('Error: The first known point must be at x=0.')
        return -1
    x_i = np.array(known_points[0])
    y_i = np.array(known_points[1])
    interp = PchipInterpolator(x_i, y_i)
    try:
        poly = PPoly.from_bernstein_basis(interp, extrapolate=None)
    except TypeError:
        # already a PPoly instance, nothing to do
        poly = interp
    coefs = poly.c.T
    number_of_pieces = len(coefs)
    length_of_pieces = []
    for j in range(number_of_pieces):
        length_of_pieces.append(cclength(coefs[j], x_i[j + 1] - x_i[j]))
    return np.hstack([np.array([0]), np.cumsum(np.array(length_of_pieces))])
