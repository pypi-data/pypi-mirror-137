import math
import numpy as np
from io import BytesIO
from os.path import exists, join, abspath, sep
from os import makedirs
from PIL import Image
import requests
from itertools import product
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
import urllib
import codecs

xyz_servers_url = {'opentopomap': 'https://opentopomap.org/{z}/{x}/{y}.png',
                   'openstreetmap': 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                   'google terrain': 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
                   'esri world imagery': 'https://server.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}.png'}


def url_to_path(url, exclude_last_part=False):
    """ Converts an url to a path

     Parameters
     ----------
     url: str
        url to convert

    exclude_last_part: bool, default: False
        If True, the part after the last slash in the url is omitted

    Returns
    -------
    str
        encoded path string
    """
    p = [urllib.parse.urlsplit(url).scheme, urllib.parse.urlsplit(url).netloc]
    p += urllib.parse.urlsplit(url).path.split('/')
    q = [codecs.encode(codecs.encode(i, 'utf8'), 'hex').decode('utf-8') for i in p[:-1]]
    if exclude_last_part:
        p = q
    else:
        p = q + [p[-1]]
    p = sep.join(p)
    return p


def path_to_url(p):
    """ Converts an url encoded with url_to_path as a path back to an url

    Parameters:
    ___________
    p: str
        encoded path string to convert

    Returns
    -------
    str
       url string
    """
    p = [codecs.decode(i, 'hex').decode('utf-8') for i in p.split(sep)]
    url = p[0] + '://' + p[1] + '/'.join(p[2:])
    return url


def deg2num(lon, lat, zoom, tile_size=256):
    """ Converts WGS84 coordinates (EPSG:4326) to web pseudo-mercator coordinates (EPSG:3758)

    Parameters
    ----------
    lon: float
        longitude in decimal degrees
    lat: float
        latitude in decimal degrees
    zoom: int
        zoom level
    tile_size: int
        size of the side of a square tile in pixels

    Returns
    -------
    tuple
        (x, y) planar coordinates in web pseudo-mercator coordinate system
    """
    r = math.pow(2, zoom) * tile_size
    lat = math.radians(lat)

    x = int((lon + 180.0) / 360.0 * r)
    y = int((1.0 - math.log(math.tan(lat) + (1.0 / math.cos(lat))) / math.pi) / 2.0 * r)

    return x, y


def get_image_cluster(left, top, right, bottom, zoom, xyz_server_url, tile_size=256, cache_dir='./.tiles_cache',
                      verbose=False):
    """ Gets a cluster of tiles from a xyz server, assembles it and crops it to the given extent

    Parameters
    ----------
    left: float
        longitude in degrees of the top left corner
    top: float
        latitude in degrees of the top left corner
    right: float
        longitude in degrees of the bottom right corner
    bottom: float
        latitude in degrees of the bottom right corner
    zoom: int
        zoom level
    xyz_server_url: str
        url of the xyz server
    tile_size: int
        size of the side of a square tile in pixels
    cache_dir: str, default: './.tiles_cache'
        path to a directory to cache the tiles
    verbose: bool
        verbose output if True

    Returns
    -------
    tuple
        (image, extent)
    """

    ## xyz_server_url = xyz_server_url.split('https://', maxsplit=1)[0]
    x0, y0 = deg2num(left, top, zoom, tile_size)
    x1, y1 = deg2num(right, bottom, zoom, tile_size)

    x0_tile, y0_tile = int(x0 / tile_size), int(y0 / tile_size)
    x1_tile, y1_tile = math.ceil(x1 / tile_size), math.ceil(y1 / tile_size)

    number_of_tiles = (x1_tile - x0_tile) * (y1_tile - y0_tile)
    if verbose:
        print(f'Requesting {number_of_tiles}...')
    assert number_of_tiles < 50, "That's too many tiles!"

    # full size image we'll add tiles to
    img = Image.new('RGB', ((x1_tile - x0_tile) * tile_size, (y1_tile - y0_tile) * tile_size))

    # loop through every tile inside our bounded box
    z = zoom

    for x, y in product(range(x0_tile, x1_tile), range(y0_tile, y1_tile)):
        cache_filename = join(cache_dir, url_to_path(xyz_server_url.format(x=x, y=y, z=zoom)))
        if not exists(cache_filename):
            if verbose:
                print('Getting tile ' + xyz_server_url.format(x=x, y=y, z=zoom) + ' ...')
            with requests.get(xyz_server_url.format(x=x, y=y, z=zoom)) as resp:
                tile_img = Image.open(BytesIO(resp.content))
                if cache_dir is not None:
                    cache_filepath = join(cache_dir, url_to_path(xyz_server_url.format(x=x, y=y, z=zoom),
                                                                 exclude_last_part=True))
                    makedirs(cache_filepath, exist_ok=True)
                    tile_img.save(cache_filename.format(x=x, y=y, z=zoom), format='png')
        else:
            if verbose:
                print(f'Retrieving ' + xyz_server_url.format(x=x, y=y, z=zoom) + f' from cache {abspath(cache_dir)}...')
            tile_img = Image.open(cache_filename)
            # add each tile to the full size image
        img.paste(
            im=tile_img,
            box=((x - x0_tile) * tile_size, (y - y0_tile) * tile_size))

    x, y = x0_tile * tile_size, y0_tile * tile_size

    img = img.crop((int(x0 - x), int(y0 - y), int(x1 - x), int(y1 - y)))
    extent = (left, right, bottom, top)
    aspect_ratio = 1/np.cos(np.radians(np.mean([top, bottom])))

    return img, extent, aspect_ratio


def auto_zoom_level(extent, max_zoom=17):
    """ Automatic determination of the zoom level to retrieve tiles from a xyz tile server

    Parameters
    ----------
    extent: tuple
        (longitude of left border, longitude of right border, latitude of bottom border, latitude of top border)
    max_zoom: int, default: 17
        maximum zoom level

    Returns
    -------
    int
        zoom level to retrieve tiles
    """

    left, right, bottom, top = extent
    s = min([np.radians(right - left) * 6378137. * np.cos(np.radians(np.mean([top, bottom]))),
             6378137. * np.radians(top - bottom)])
    zoom_level = np.max([1, np.min([max_zoom, int(np.floor(np.log((5 * 2 * np.pi * 6378137. *
                                                                   np.cos(np.radians(np.mean([top, bottom])))) / s) /
                                                           np.log(2)))])])
    return zoom_level


def plot_basemap(extent, ax=None, **kwargs):
    """ Plots a basemap and returns a matplotlib axes

    Parameters
    ----------
    extent: tuple
        (longitude of left border, longitude of right border, latitude of bottom border, latitude of top border)
    ax: matplotlib.pyplot.axes, default: None
        an axes into which the basemap is plotted
    dms: bool
        True if latitude and longitudes should be displayed in DD°MM'SS.SSS'' format
    figsize: tuple, default: (16,8)
        size of the figure
    grid: str, default: 'on'
        'on' to show the grid, 'off' to hide the grid
    zoom: int
        zoom level
    max_zoom: int, default: 17
        maximum zoom level
    xyz_server: str, default: 'opentopomap'
        name or url of the xyz server
    tile_size: int, default=256
        size of the side of a square tile in pixels
    cache_dir: str, default: './.tiles_cache'
        path to a directory to cache the tiles
    verbose: bool
        verbose output if True
    """
    left, right, bottom, top = extent
    xyz_server = kwargs.pop('xyz_server', 'opentopomap')
    if xyz_server not in xyz_servers_url.keys():
        xyz_server_url = xyz_server
    else:
        xyz_server_url = xyz_servers_url[xyz_server.lower()]
    max_zoom = kwargs.pop('max_zoom', 17)
    zoom = kwargs.pop('zoom', auto_zoom_level(extent, max_zoom))

    if ax is None:
        _, ax = plt.subplots(figsize=kwargs.pop('figsize', (16, 8)))

    img, extent, ratio = get_image_cluster(left, top, right, bottom, zoom, xyz_server_url,
                                           tile_size=kwargs.pop('tile_size', 256),
                                           cache_dir=kwargs.pop('cache_dir', './.tiles_cache'),
                                           verbose=kwargs.pop('verbose', False))
    ax.imshow(img, extent=extent, aspect=ratio)
    ax.set_xlim(left, right)
    ax.set_ylim(bottom, top)
    dms = kwargs.pop('dms', True)
    if dms:
        ax.xaxis.set_major_formatter(
            FuncFormatter(lambda x, pos: f"{x // 1:.0f}° {(x % 1) * 60:02.0f}' {((x % 1) % 60) * 60:02.2f}''"))
        ax.yaxis.set_major_formatter(
            FuncFormatter(lambda x, pos: f"{x // 1:.0f}° {(x % 1) * 60:02.0f}' {((x % 1) % 60) * 60:02.2f}''"))
    else:
        ax.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: f"{x:02.2f}°"))
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f"{x:02.2f}°"))

    ax.grid(kwargs.pop('grid', 'on'))
    return ax
