from django.contrib.gis.geos import GEOSGeometry, Polygon, MultiPolygon
import geopandas as gpd


def load_layer(geojson_file):

    #layer_gdf = gpd.read_file('qml/data/json/dpaw_regions.json')
    layer_gdf = gpd.read_file(geojson_file)
    srid = int(layer_gdf.crs.srs.split(':')[1])
    layer = Layer.objects.create(name='dpaw_regions', type='cddp', srid=int(layer_gdf.crs.srs.split(':')[1]), geojson=layer_gdf.to_json())


    # create the layer features/geometries
    for idx, row in layer_gdf.iterrows():
	#print(idx, row)
	cols = list(row.keys())
	cols.remove('geometry')
	attributes = row[cols].to_dict()
	geom_str = str(row.geometry)
	geometry = GEOSGeometry( geom_str )
	feature = Feature.objects.create(attributes=attributes, geometry=geometry, layer=layer)
