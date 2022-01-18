from django.contrib.gis.geos import GEOSGeometry, Polygon, MultiPolygon
from django.conf import settings

import geopandas as gpd
import requests
import json
import os

from qml.components.masterlist.models import Layer, Feature#, LayerHistory, Feature

class LayerLoader():
    """
    In [22]: from qml.utils.utils import LayerLoader
    In [23]: l=LayerLoader(url,name)
    In [24]: l.load_layer()


    In [23]: layer=Layer.objects.last()
    In [25]: layer.feature_features.all().count()
    Out[25]: 9

    In [25]: layer.srid
    Out[25]: 4326

    """

    def __init__(self, url, name):
        self.url = url
        self.type = name.split(':')[0]
        self.name = name.split(':')[1]
        
    def retrieve_layer(self):
        try:
            res = requests.get('{}'.format(self.url), auth=(settings.KMI_USER,settings.KMI_TOKEN), verify=False)
            res.raise_for_status()
            #cache.set('department_users',json.loads(res.content).get('objects'),10800)
            return res.json()
        except:
            raise

    def load_layer(self):

        #layer_gdf = gpd.read_file('qml/data/json/dpaw_regions.json')
        #layer_gdf = gpd.read_file(io.BytesIO(geojson_str))
        geojson = self.retrieve_layer()
        layer = Layer.objects.create(name=self.name, type=self.type, geojson=geojson)

        # create the layer features/geometries
        layer_gdf = gpd.read_file(json.dumps(geojson))
        for idx, row in layer_gdf.iterrows():
            #print(idx, row)
            cols = list(row.keys())
            cols.remove('geometry')
            attributes = row[cols].to_dict()
            geom_str = str(row.geometry)
            geometry = GEOSGeometry( geom_str )
            feature = Feature.objects.create(attributes=attributes, geometry=geometry, layer=layer)
