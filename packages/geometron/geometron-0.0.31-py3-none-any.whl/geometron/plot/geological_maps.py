import matplotlib.path as mpath
import matplotlib.patches
import matplotlib.pyplot as plt
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
from matplotlib.transforms import Affine2D
import numpy as np
from warnings import warn


def plot_map(polygon_dict, color_dict, extent, ax=None, **kwargs):
    if ax is None:
        fig, ax = plt.subplots()

    for k in polygon_dict.keys():
        paths = polygon_dict[k]
        for p in paths:
            polygon_patch = matplotlib.patches.PathPatch(p, facecolor=color_dict[k], **kwargs)
            ax.add_patch(polygon_patch)
    ax.set_xlim([extent[0], extent[1]])
    ax.set_ylim([extent[2], extent[3]])
    ax.set_aspect(1.)


def plot_observations(gdf_surface_points, gdf_orientations, color_dict=None, field='formation',
                      title='', label='Z', label_unit='m', ax=None, extent=None, add_legend=True):
    if ax is None:
        fig, ax = plt.subplots()

    if extent is None:
        extent = [0., 100., 0., 100.]  # TODO: Compute extent from the geodataframes

    for category, data in gdf_surface_points.groupby(field):
        data.plot(color=color_dict[category],
                  ax=ax,
                  label=category,
                  markersize=75)
        for idx, row in data.iterrows():
            ax.text(row.geometry.x, row.geometry.y, f'# {idx}\n z={row[label]}\n', fontsize=10, va='bottom',
                    ha='center')

    for idx, row in gdf_orientations.iterrows():
        patch, txt_patch = dip_and_strike_patch((row.geometry.x, row.geometry.y), row['dip'], row['azimuth'] - 90,
                                                size=2, fc='k',
                                                ec=color_dict[row[field]], linewidth=2)
        ax.add_patch(patch)
        ax.add_patch(txt_patch)
        ax.text(row.geometry.x, row.geometry.y, f'\n # {idx}\n', fontsize=10, va='top', ha='center')
    ax.set_title(title)
    if add_legend:
        ax.legend(fontsize=16, frameon=True, loc='best', title=field.capitalize())
    ax.grid('on')
    ax.set_xlim([extent[0], extent[1]])
    ax.set_ylim([extent[2], extent[3]])
    return ax


def dip_and_strike_patch(xy, dip=0., strike=0., polarity=1, size=1., degrees=True, **kwargs) \
        -> (matplotlib.patches.Patch, matplotlib.patches.Patch):
    """ Creates a symbol to represent structural information for bedding observation

    Parameters
    ----------
    xy : tuple
        2d coordinates of the observation
    dip : float, default 0.
        angle
    strike : float
        is the angle
    polarity : {1,0}
        1 for normal polarity, 0 for reversed polarity
    size : float
        size of the symbol in the map units
    degrees : bool, default True
        True if dip and strike angles are given in degrees, False if they are given in radians
    kwargs : dict
        arguments passed to build the patches

    Returns
    -------
    (matplotlib.patches.Patch, matplotlib.patches.Patch)

    """
    # patch = None
    # txt_patch = None
    if 'linewidth' not in kwargs.keys():
        kwargs['linewidth'] = 4.
    if 'facecolor' not in kwargs.keys():
        if 'fc' not in kwargs.keys():
            kwargs['facecolor'] = 'black'
        else:
            kwargs['facecolor'] = kwargs['fc']
    x, y = xy

    if degrees:
        dip = np.deg2rad(dip)
        strike = np.deg2rad(strike)
    if dip > np.pi / 2 or dip < 0.:
        warn('Unexpected value for dip : {np.degrees(dip):0.f} ! Dip should be between 0° and 90°...')
        bad_dip = True
    else:
        bad_dip = False

    polarity = polarity // 1
    strike = strike % (2 * np.pi)
    # print(f'dip:{np.degrees(dip):.0f}°, strike:{np.degrees(strike):.0f}°, polarity: {polarity}')

    s = size * np.sin(strike)
    c = size * np.cos(strike)
    x_start, x_end = x + s, x - s
    y_start, y_end = y + c, y - c
    x_dip = x + c * (0.1 + 0.9 * np.cos(dip))
    y_dip = y - s * (0.1 + 0.9 * np.cos(dip))

    if dip == 0.:
        # To create a cross and
        # approximate a circle with cubic Bézier curves cf. https://spencermortensen.com/articles/bezier-circle/
        f = 0.551915024494 * size
        path_data = [(mpath.Path.MOVETO, (x - size, y)), (mpath.Path.LINETO, (x + size, y)),
                     (mpath.Path.MOVETO, (x, y - size)), (mpath.Path.LINETO, (x, y + size)),
                     (mpath.Path.LINETO, (x, y + size)), (mpath.Path.CURVE4, (x + f, y + size)),
                     (mpath.Path.CURVE4, (x + size, y + f)), (mpath.Path.CURVE4, (x + size, y)),
                     (mpath.Path.CURVE4, (x + size, y - f)), (mpath.Path.CURVE4, (x + f, y - size)),
                     (mpath.Path.CURVE4, (x, y - size)),
                     (mpath.Path.CURVE4, (x - f, y - size)), (mpath.Path.CURVE4, (x - size, y - f)),
                     (mpath.Path.CURVE4, (x - size, y)),
                     (mpath.Path.CURVE4, (x - size, y + f)), (mpath.Path.CURVE4, (x - f, y + size)),
                     (mpath.Path.CURVE4, (x, y + size))
                     ]
        kwargs['facecolor'] = 'none'
        kwargs['fc'] = 'none'
        codes, verts = zip(*path_data)
        path = mpath.Path(verts, codes)
        patch = matplotlib.patches.PathPatch(path, **kwargs)
        txt_patch = None
    else:
        path_data = [(mpath.Path.MOVETO, (x_start, y_start)), (mpath.Path.LINETO, (x_end, y_end)),
                     (mpath.Path.MOVETO, (x, y))]
        if dip == 90.:
            path_data = [(mpath.Path.MOVETO, (x_start, y_start)), (mpath.Path.LINETO, (x_end, y_end)),
                         (mpath.Path.MOVETO, (x - c / 4, y + s / 4)),
                         (mpath.Path.LINETO, (x + c / 4, y - s / 4))]
            codes, verts = zip(*path_data)
            path = mpath.Path(verts, codes)
            patch = matplotlib.patches.PathPatch(path, **kwargs)
            txt_patch = None
        else:
            path_data.append((mpath.Path.LINETO, (x_dip, y_dip)))
            if polarity == 0:
                path_data.append((mpath.Path.MOVETO, (x, y)))
                path_data.append((mpath.Path.CURVE4, (x - c / 4, y + s / 4)))
                path_data.append((mpath.Path.CURVE4, (x + s / 3 - c / 4, y + c / 3 + s / 4)))
                path_data.append((mpath.Path.CURVE4, (x + s / 3, y + c / 3)))
            codes, verts = zip(*path_data)
            path = mpath.Path(verts, codes)
            kwargs_txt = kwargs.copy()
            kwargs_txt['edgecolor'] = 'none'
            kwargs_txt['ec'] = 'none'
            kwargs['facecolor'] = 'none'
            kwargs['fc'] = 'none'
            patch = matplotlib.patches.PathPatch(path, **kwargs)
            fp = FontProperties(family="Liberation Sans", style="normal")
            txt_patch = matplotlib.patches.PathPatch(
                TextPath((0, 0), f' {np.degrees(dip):.0f}°', size=.8 * size, prop=fp).transformed(
                    Affine2D().translate(0, -.2 * size).rotate(-strike).translate(x_dip, y_dip)), **kwargs_txt)

    return patch, txt_patch
