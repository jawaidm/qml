from django.contrib.gis.geos import GEOSGeometry, Polygon, MultiPolygon
from django.conf import settings
from django.db import transaction

import geopandas as gpd
import requests
import json
import os

from qml.components.masterlist.models import Layer, Feature#, LayerHistory, Feature

import logging
logger = logging.getLogger(__name__)

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

    def __init__(self, url='https://kmi.dbca.wa.gov.au/geoserver/cddp/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=cddp:dpaw_regions&maxFeatures=50&outputFormat=application%2Fjson', name='cddp:jm2'):
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

    def retrieve_layer_from_file(self, filename='qml/data/json/dpaw_regions.json'):
        try:
            with open(filename) as json_file:
                data = json.load(json_file)
            return data
        except:
            raise


    def load_layer(self):

        #layer_gdf = gpd.read_file('qml/data/json/dpaw_regions.json')
        #layer_gdf = gpd.read_file(io.BytesIO(geojson_str))
        #import ipdb; ipdb.set_trace()

        #geojson = self.retrieve_layer()
        #layer_gdf1 = gpd.read_file(json.dumps(geojson))
        geojson = self.retrieve_layer_from_file()
        layer_gdf1 = gpd.read_file(json.dumps(geojson))

        layer_qs = Layer.objects.filter(name=self.name, type=self.type, current=True)
        current_layer = None
        if layer_qs.count() == 1:
            current_layer = layer_qs[0]
            #import ipdb; ipdb.set_trace()
            layer_gdf2 = gpd.read_file(json.dumps(current_layer.geojson))

            if not layer_changed(layer_gdf1, layer_gdf2):
                # no change in geojson
                logger.info(f'LAYER NOT UPDATED: No change in layer') 
                return

        with transaction.atomic():
            if current_layer:
                current_layer.current = False
                current_layer.save()

            layer = Layer.objects.create(name=self.name, type=self.type, geojson=geojson, current=True)

            # create the layer features/geometries
            #layer_gdf1 = gpd.read_file(json.dumps(geojson))
            for idx, row in layer_gdf1.iterrows():
                #print(idx, row)
                cols = list(row.keys())
                cols.remove('geometry')
                attributes = row[cols].to_dict()
                geom_str = str(row.geometry)
                geometry = GEOSGeometry( geom_str )
                feature = Feature.objects.create(attributes=attributes, geometry=geometry, layer=layer)

            logger.info(f'Created Layer: {layer}, with {layer.feature_features.count()} features, srid {layer.srid}') 


#            layer, created = Layer.objects.update_or_create(
#                name=self.name,
#                type=self.type,
#                defaults={
#                    'geojson': geojson 
#                }
#            )
#
#            if not created:
#                layer.feature_features.all().delete() 


  
  
def layer_changed(layer_gdf1, layer_gdf2):

    # check columns are the same
    cols1 = list(layer_gdf1.columns.sort_values())
    cols2 = list(layer_gdf2.columns.sort_values())
    if cols1 != cols2:
        # GeoJSON has changed
        return True

    # remove the 'id' column from layer_gdf's and sort the columns [index(axis=1)]
    layer_gdf1 = layer_gdf1.loc[:, layer_gdf1.columns!='id'].sort_index(axis=1)
    layer_gdf2 = layer_gdf2.loc[:, layer_gdf2.columns!='id'].sort_index(axis=1)

    # check geo dataframes are the same
    if (layer_gdf1 == layer_gdf2).eq(True).all().eq(True).all():
        # GeoJSON has not changed
        return False

    return True

