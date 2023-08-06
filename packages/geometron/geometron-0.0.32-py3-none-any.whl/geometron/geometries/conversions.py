import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon
import numpy as np


def gdf_to_points_gdf(gdf, columns=None):
    if columns is None:
        columns = []
    geo_interface = {"type": "FeatureCollection"}
    features = []
    bbox = (gdf.iloc[:]['geometry'].bounds.minx.min(), gdf.iloc[:]['geometry'].bounds.maxx.max(),
            gdf.iloc[:]['geometry'].bounds.miny.min(), gdf.iloc[:]['geometry'].bounds.maxy.max())
    geo_interface["bbox"] = bbox
    point_id = 0
    for idx, row in gdf.iterrows():
        if isinstance(row['geometry'], Polygon):
            polygon = row['geometry']
            vertices = np.array(polygon.exterior.coords[:])
            for j in range(vertices.shape[0]):
                properties = {p: row[p] for p in columns}
                pt = {"id": f'{point_id}', "type": "Feature", "properties": properties,
                      "geometry": {"type": "Point", "coordinates": tuple(vertices[j, :])}
                      }
                features.append(pt)
                point_id += 1
        elif isinstance(row['geometry'], LineString):
            linestring = row['geometry']
            vertices = np.array(linestring.coords[:])
            for j in range(vertices.shape[0]):
                properties = {p: row[p] for p in columns}
                pt = {"id": f'{point_id}', "type": "Feature", "properties": properties,
                      "geometry": {"type": "Point", "coordinates": tuple(vertices[j, :])}
                      }
                features.append(pt)
                point_id += 1
        elif isinstance(row['geometry'], Point):
            point = row['geometry']
            properties = {p: row[p] for p in columns}
            pt = {"id": f'{point_id}', "type": "Feature", "properties": properties,
                  "geometry": {"type": "Point", "coordinates": tuple(point.coords[:])}
                  }
            features.append(pt)
            point_id += 1
        else:
            print(f'Warning: gdf_to_points_gdf cannot process {type(row["geometry"])} geometries. '
                  f'These geometries will be ignored.')
    geo_interface["features"] = features

    return gpd.GeoDataFrame.from_features(geo_interface)
