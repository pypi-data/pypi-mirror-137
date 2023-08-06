import matplotlib.pyplot as plt
import numpy as np
import shapely.wkb
from shapely.geometry import Point, LineString, LinearRing, Polygon, MultiPoint, MultiLineString
from descartes import PolygonPatch


def plot_shapely_obj(obj=None, ax=None, **kwargs):
    """ Plots a shapely object in matplotlib axes

    Parameters
    ----------
    obj : shapely.geometry
        A shapely object to plot
    ax : matplotlib.axes
        Axes in which the shapely object should be plotted
    kwargs : dict
        Keywords and arguments to pass to matplotlib plot for Point, MultiPoint, LineString, MultiLineString or
        LinearStrings and to patches for polygons

    Returns
    -------
        the matplotlib axes object used to plot the shapely object
    """
    if ax is None:
        fig, ax = plt.subplots()
        ax.axis('equal')
    if isinstance(obj, Point) or isinstance(obj, LineString) or isinstance(obj, LinearRing):
        x, y = obj.xy
        ax.plot(x, y, **kwargs)
    elif isinstance(obj, MultiLineString) or isinstance(obj, MultiPoint):
        for i in obj:
            plot_shapely_obj(ax=ax, obj=i, **kwargs)
    elif isinstance(obj, Polygon):
        patch = PolygonPatch(obj, **kwargs)
        ax.add_patch(patch)
    else:
        print(f'Warning:Invalid object type - {obj} : {type(obj)}...')
    ax.axis('equal')
    return ax


def plot_profile(ax=None, obj=None, name=''):
    if isinstance(obj, LineString):
        ax = plot_shapely_obj(ax=ax, obj=obj, color='k', linestyle='--', linewidth=0.75)
        plot_shapely_obj(ax=ax, obj=Point(obj.coords[0]), marker='o', color='g')  # start
        for i in range(1, len(obj.coords)):
            plot_shapely_obj(ax=ax, obj=Point(obj.coords[i]), marker='x', color='grey')
        plot_shapely_obj(ax=ax, obj=Point(obj.coords[-1]), marker='s', color='r')  # end
        theta = np.arctan2(obj.coords[-1][1] - obj.coords[0][1], obj.coords[-1][0] - obj.coords[0][0]) * 180. / np.pi
        ax.text(obj.centroid.coords[0][0], obj.centroid.coords[0][1], name, rotation=theta,
                horizontalalignment='center', verticalalignment='top', multialignment='center')
        ax.axis('equal')
    return ax
