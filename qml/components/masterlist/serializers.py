from django.conf import settings
from django.db.models import Q

from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
#from reversion.models import Version

#from ledger.accounts.models import EmailUser,Address
#from commercialoperator.components.main.models import ApplicationType
from qml.components.masterlist.models import (
    Layer,
    LayerHistory,
    Feature,
)


class GeoTestSerializer(serializers.ModelSerializer):
    #accreditation_type_value= serializers.SerializerMethodField()
    #accreditation_expiry = serializers.DateField(format="%d/%m/%Y",input_formats=['%d/%m/%Y'],required=False,allow_null=True)

    class Meta:
        model = Layer
        #fields = '__all__'
        fields=(
            'id',
            'name',
            'type',
        )

    #def get_accreditation_type_value(self,obj):
    #    return obj.get_accreditation_type_display()


#class FeatureGeometrySerializer(serializers.ModelSerializer):
class FeatureGeometrySerializer(GeoFeatureModelSerializer):

    class Meta:
        model = Feature
        geo_field = 'geometry'
        fields=(
            'id',
            'srid',
            'geometry',
        )

    def get_properties(self, obj, fields):
        ''' override the rest_framework_gis/serializers.get_properties() method to add the attributes fields '''
        feature_properties = super(FeatureGeometrySerializer, self).get_properties(obj, fields)
        feature_properties.update(obj.properties)
        return feature_properties


class LayerSerializer(serializers.ModelSerializer):
    #features = FeatureGeometrySerializer(source='feature_features', many=True, read_only=True)

    class Meta:
        model = Layer
        geo_field = 'geojson'
        fields=(
            'id',
            'name',
            'type',
            'srid',
            'current',
            'version',
            #'features',
            'geojson',
        )


