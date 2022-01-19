from django.contrib.gis.geos import GEOSGeometry, Polygon, MultiPolygon
from django.conf import settings
from django.db import transaction

import geopandas as gpd
import requests
import json
import os

from qml.components.masterlist.models import Layer, Feature#, LayerHistory

import logging
logger = logging.getLogger(__name__)


class GeoQueryHelper():

    def __init__(self, layer):
        self.layer = layer

    def filter_dict(self, feature, required_attributes):
        return dict((key,value) for key, value in feature.attributes.items() if key in required_attributes)

    def intersection(self, required_attributes):

        #with open('qml/data/json/south_wa.json') as f:
        with open('qml/data/json/goldfields.json') as f:
            polygon_geojson = json.load(f)

        intersection_geom = []
        for ft in polygon_geojson['features']:
            geom_str = json.dumps(ft['geometry'])
            geom = GEOSGeometry(geom_str)
            try:
                if isinstance(geom, MultiPolygon):
                    continue

                elif isinstance(geom, Polygon):
                    geom = MultiPolygon([geom])
             
                    #for region in DpawRegion.objects.filter(geom__intersects=geom):
                    #import ipdb; ipdb.set_trace()
                    for feature in self.layer.feature_features.filter(geometry__intersects=geom):
                        #intersection_geom.append(geom.intersection(feature.geometry))
                        intersection_geom.append(self.filter_dict(feature, required_attributes))
                        #print(feature)
                    #import ipdb; ipdb.set_trace()
                print(intersection_geom)
            except TypeError as e:
                print(e)
