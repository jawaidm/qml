from django.conf import settings
from django.db.models import Q

from rest_framework import serializers
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


#class FeatureSerializer(serializers.RelatedField):
class FeatureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feature
        fields=(
            'id',
            'attributes',
            'srid',
        )

class LayerSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(source='feature_features', many=True, read_only=True)

    class Meta:
        model = Layer
        fields=(
            'id',
            'name',
            'type',
            'srid',
            'current',
            'version',
            'features',
        )


