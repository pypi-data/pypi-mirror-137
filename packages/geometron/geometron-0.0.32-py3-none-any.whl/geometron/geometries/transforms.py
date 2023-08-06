import geopandas
import numpy as np
import shapely
from shapely.geometry import Point, LineString, Polygon


def flatten_geometry(obj):
    """ Takes a 3D geometry and returns a 2D geometry discarding the third coordinate
    Parameters
    ----------
    obj : shapely.geometry
        a 3D geometry to flatten

    Returns
    -------
    shapely.geometry
        a 2D geometry
    """

    return shapely.wkb.loads(shapely.wkb.dumps(obj, output_dimension=2))


def raise_geometry(obj, elevation=0.):
    """ Turns a 2d geometry or 2d geometries of a geodataframe in 3d geometry(ies) with the given constant elevation,
    if obj is a geodataframe, the transform is done in place.

    Parameters
    ----------
    obj : shapely.geometry or geopandas.GeoDataFrame
        the geometry
    elevation : float
        elevation to which obj will be raised

    Returns
    -------
    shapely.geometry or geopandas.GeoDataFrame
        modified géometry(ies)

    Examples
    --------
    >>> # This example shows how to raise a 2D Point to a 3D point with elevation set to 100.
    >>> from shapely.geometry import Point
    >>> from geometron.geometries.transforms import raise_geometry
    >>> p = Point([1., 3.])
    >>> p = raise_geometry(p, 100.)
    >>> print(p)
    POINT Z (1 3 100)
    """

    if isinstance(obj, geopandas.GeoDataFrame):
        for idx, row in obj.iterrows():
            g = row['geometry']
            if g.geom_type == 'Point':
                coords = [(i[0], i[1], elevation) for i in row['geometry'].coords]
                obj.loc[idx, 'geometry'] = Point(coords)
            elif g.geom_type == 'LineString':
                coords = [(i[0], i[1], elevation) for i in row['geometry'].coords]
                obj.loc[idx, 'geometry'] = LineString(coords)
            elif g.geom_type == 'Polygon':
                # exterior ring
                exterior = [(i[0], i[1], elevation) for i in g.exterior.coords]
                # interior rings (a.k.a. holes)
                interiors = [[(j[0], j[1], elevation) for j in i.coords] for i in g.interiors]
                obj.loc[idx, 'geometry'] = Polygon(exterior, interiors)
    elif obj.geom_type == 'Point':
        coords = [(i[0], i[1], elevation) for i in obj.coords]
        obj = Point(coords)
    elif obj.geom_type == 'LineString':
        coords = [(i[0], i[1], elevation) for i in obj.coords]
        obj = LineString(coords)
    elif obj.geom_type == 'Polygon':
        # exterior ring
        exterior = [(i[0], i[1], elevation) for i in obj.exterior.coords]
        # interior rings (a.k.a. holes)
        interiors = [[(j[0], j[1], elevation) for j in i.coords] for i in obj.interiors]
        obj = Polygon(exterior, interiors)
    return obj


def rotate_around_vector(vector, angle, degrees=False, affine_4x4=False):
    """Returns the matrix associated to a rotation by a given angle around a given vector using Rodrigues formula

    Parameters
    ----------
    vector : numpy.array
        vector around which the rotation matrix will be computed
    angle : float
        amplitude of rotation given following the right-hand-side rule
    degrees : bool, default: False
        set to True if angle is given in degrees rather than in radians
    affine_4x4 : bool, default: False
        set to True to return a 4x4 affine transform matrix

    Returns
    -------
    numpy.array
        transform matrix

    Example
    -------
    >>> # This example shows how to use this function to rotate by 90° a given vector a around vector v.
    >>> import numpy as np
    >>> import geometron.geometries.transforms as ggt
    >>> a = np.array([0., 0., 1.])
    >>> v = np.array([3., 0., 0.])
    >>> angle = np.pi/2
    >>> r = ggt.rotate_around_vector(v, angle)
    >>> np.dot(r, a)
    array([ 0.00000000e+00, -1.00000000e+00,  1.11022302e-16])
    For more info. see https://en.wikipedia.org/wiki/Rodrigues'_rotation_formula#Matrix_notation
    """

    vector = np.array(vector)  # convert array-like (list, tuple) into a numpy array
    vector = vector/np.linalg.norm(vector)  # normalize the vector
    if degrees:
        # convert degrees to radians
        angle = angle * np.pi / 180.
    c = np.array([[0., -vector[2], vector[1]], [vector[2], 0., -vector[0]], [-vector[1], vector[0], 0.]])
    r = np.eye(3) + c * np.sin(angle) + np.matmul(c, c) * (1 - np.cos(angle))
    if affine_4x4:
        r = np.vstack([r, np.array([0., 0., 0.])])
        r = np.hstack([r, np.array([[0., 0., 0., 1.]]).T])
    return r


def affine_transform_matrix(origin_coords, destination_coords, rcond=-1, shapely_format=True):
    """ Computes a transform matrix to use on shapely or vtk objects from control points coordinates

    origin_coords : list, numpy.array
        2D or 3D coordinates of the control points in the origin space
    destination_coords : list, numpy.array
        2D or 3D coordinates of the control points in the destination space
    rcond : float, default: -1
        Cut-off ratio for small singular values used by numpy.linalg.lstsq
    shapely_format : bool, default: True
        If True, returns a transform matrix in the shapely format otherwise returns a 3x3 or 4x4 transform matrix

    Returns
    -------
    matrix : numpy.array, list
        The transform matrix (in list form if shapely_format is True)
    residuals : numpy.array
        The residuals of the least-squares fitting of the parameters of the transform from the control points coordinate
         pairs
    rank : int
        Rank of matrix a
    singular: (min(M, N),) ndarray
        Singular values of a

    Example
    -------
    >>> # This example shows how to use this function to compute the affine transform matrix from 2D control points.
    >>> import numpy as np
    >>> import geometron.geometries.transforms as ggt
    >>> origin_coords = [np.array([0.,0.]), np.array([0.,1.]), np.array([1.,0.]), np.array([1.,1.2])]
    >>> destination_coords = [np.array([2.5,1.5]), np.array([2.,2.]), np.array([3.,2.]), np.array([2.5,3.])]
    >>> transform_matrix, residuals, rank, singular = ggt.affine_transform_matrix(origin_coords, destination_coords)
    >>> transform_matrix
    [0.5450819672131152, -0.4508196721311477, 0.6803278688524602,
    0.6967213114754098, 2.4754098360655745, 1.401639344262296]

    """
    if isinstance(origin_coords, list):
        origin_coords = np.array(origin_coords)
    if isinstance(destination_coords, list):
        destination_coords = np.array(destination_coords)

    n_pts, dim = origin_coords.shape
    assert destination_coords.shape[0] == n_pts
    assert destination_coords.shape[1] == dim

    a = np.vstack([origin_coords.T, np.ones([1, n_pts])]).T
    b = destination_coords
    transform_matrix, residuals, rank, singular = np.linalg.lstsq(a, b, rcond=rcond)
    transform_matrix = np.vstack([transform_matrix.swapaxes(0, 1), np.hstack([np.zeros([1, dim]), np.ones([1, 1])])])
    if shapely_format:
        transform_matrix = list(np.hstack([transform_matrix[:-1, :dim].flatten(),
                                           transform_matrix[:-1, dim:].flatten()]))
    return transform_matrix, residuals, rank, singular
