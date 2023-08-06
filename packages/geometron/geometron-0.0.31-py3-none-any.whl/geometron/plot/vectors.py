import numpy as np
from pyvista import Plotter, Arrow
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, AutoMinorLocator


def plot_3d_vectors(vectors, origins=None, colors=None, add_labels=False, names=None, plotter=None, tip_length=0.25,
                    tip_radius=0.1, shaft_radius=0.05, show_grid=False):
    """ Plots 3D vectors in a pyvista plotter

    Parameters
    ----------
    vectors: numpy.array
        3D vectors stored as an nx3 array
    origins: numpy.array, default None
        origin point of each 3D vector in vectors
    colors: list, defaut None
        color of each 3D vector in vector
    add_labels: bool, default False
        if True, labels stored in names are added close to the vector tip (not supported by some backends)
    names: list, default None
        name for each 3D vector in vectors
    plotter: pyvista.Plotter, default None
        plotter to add the vector arrows to
    tip_length: float, default 0.25
        length of the arrow tip
    tip_radius: float, default 0.1
        radius of the arrow tip
    shaft_radius: float, default 0.05
        radius of the arrow shaft

    Returns
    -------
    pyvista.Plotter
        a plotter that includes the vectors displayed as arrows

    Examples
    ---------
    This examples shows how to display some vectors in 3D
    >>> import numpy as np
    >>> from geometron.plot import plot_3d_vectors
    >>> from geometron.geometries import vectors as ggv
    >>> plotter = plot_3d_vectors(np.vstack([2*ggv.ux, ggv.uy, ggv.uz]), colors=['red', 'blue', 'green'])
    >>> plotter.add_axes()
    >>> plotter.show(jupyter_backend='panel')
    """

    if len(vectors.shape) == 1:
        vectors = np.array([vectors])
    if origins is None:
        origins = np.zeros([len(vectors), 3])
    elif len(origins.shape) == 1:
        origins = np.array([origins]).repeat(vectors.shape[0], axis=0)
    if colors is None:
        colors = ['w' for i in range(len(vectors))]

    if plotter is None:
        plotter = Plotter()

    for i in range(vectors.shape[0]):
        scale = np.linalg.norm(vectors[i])
        tl = tip_length / scale
        tr = tip_radius / scale
        sr = shaft_radius / scale
        plotter.add_mesh(Arrow(start=origins[i], direction=vectors[i], tip_length=tl, tip_radius=tr,
                                  shaft_radius=sr, scale=scale), color=colors[i])
        if add_labels:
            plotter.add_point_labels(vectors[i], [names[i]], italic=True, font_size=20)
    if show_grid:
        plotter.show_grid()
    return plotter


def plot_2d_vectors(vectors, origins=None, colors=None, ax=None, show_grid=False):
    """ Plots 2D vectors

    Parameters
    ----------
    vectors: numpy.array or list
        2D vectors to plot
    origins: numpy.array, default None
        origin point of each 2D vector in vectors
    colors: list, defaut None
        color of each 2D vector in vector
    ax: matplotlib.axes.Axes, defaut None
        a matplotlib axes to draw the vectors
    show_grid: bool, default False
        if True, displays the grids
    Returns
    -------
    matplotlib.axes.Axes
        a matplotlib axes that includes the 2D vectors displayed as arrows

    Examples
    --------
    This examples shows how to display some vectors in 2D
    >>> import numpy as np
    >>> from geometron.plot import plot_2d_vectors
    >>> from geometron.geometries import vectors as ggv
    >>> ax = plot_2d_vectors(np.vstack([2*ggv.ux[:2], ggv.uy[:2]]), colors=['red', 'blue'], show_grid=True)
    >>> ax.show()
    """

    if len(vectors.shape) == 1:
        vectors = np.array([vectors])
    if origins is None:
        origins = np.zeros([2, len(vectors)])
    elif len(origins.shape) == 1:
        origins = np.array([origins]).repeat(vectors.shape[0], axis=0)
    if colors is None:
        colors = ['k' for i in range(len(vectors))]
    if ax is None:
        fig, ax = plt.subplots()

    ax.quiver(*origins.T, vectors[:, 0], vectors[:, 1], color=colors, angles='xy', scale_units='xy', scale=1)
    plt.axis('equal')
    # rng = np.amax(vectors) - np.amin(vectors)
    # avg = np.mean(vectors, axis=0)
    # plt.xticks(range(int(np.floor(avg[0]-rng)),int(np.ceil(avg[0]+rng))))
    # plt.yticks(range(int(np.floor(avg[1]-rng)),int(np.ceil(avg[1]+rng))))

    if show_grid:
        ax.xaxis.set_major_locator(MultipleLocator(10))
        ax.yaxis.set_major_locator(MultipleLocator(10))
        ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
        ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))

        # For the minor ticks, use no labels; default NullFormatter.
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())
        ax.grid()
    return ax
