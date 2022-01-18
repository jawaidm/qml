#from django.db import models
from django.contrib.gis.db import models
from django.contrib.postgres.fields.jsonb import JSONField
import copy


# Next lin needed, to migrate ledger_api_clinet module
from ledger_api_client.ledger_models import EmailUserRO as EmailUser

import logging
logger = logging.getLogger(__name__)


class DpawRegion(models.Model):
    fid = models.CharField(max_length=64)
    region = models.CharField(max_length=64)
    ogc_fid = models.IntegerField(null=True, blank=True)
    office = models.CharField(max_length=64, null=True, blank=True)
    hectares = models.FloatField(null=True, blank=True)
    md5_rowhash = models.CharField(max_length=64, null=True, blank=True)

    geom = models.MultiPolygonField(srid=4283)

    class Meta:
        app_label = 'qml'

    def __str__(self):
        return self.region

class Feature(models.Model):
    attributes = JSONField(db_index=True)
    geometry = models.MultiPolygonField()
    layer = models.ForeignKey('Layer', on_delete=models.CASCADE, related_name='%(class)s_features')
 
    @property
    def srid(self):
        return self.geometry.crs.srid

    class Meta:
        app_label = 'qml'

    @property
    def fid(self):
        return self.attributes['id'] if 'id' in self.attributes else 'NO_ID'

    def __str__(self):
        return f'{self.fid}'


class LayerBase(models.Model):
    name = models.CharField(max_length=64)
    type = models.CharField(max_length=32, null=True, blank=True)
    #srid = models.IntegerField(null=True, blank=True)

    geojson = JSONField('Layer GeoJSON')

    @property
    def srid(self):
        if hasattr(self, 'feature_features') and self.feature_features.exists():
            feature = self.feature_features.first()
            return feature.srid
        return None

    class Meta:
        abstract = True
        #app_label = 'qml'

    def __str__(self):
        return f'{self.type}:{self.name}' if self.type else f'{self.name}'


class Layer(LayerBase):

    current = models.BooleanField()

    @property
    def layer_history(self):
        return LayerHistory.objects.filter(layer=self).order_by('-version')

    def save(self, *args, **kwargs):
        from qml.utils.loader_utils import sorting
        super(Layer, self).save(*args, **kwargs)
        # save layer history
        import ipdb; ipdb.set_trace()
        #_layer copy.deepcopy(layer)
        layer_history = self.layer_history
        if not layer_history or sorting(self.geojson) != sorting(layer_history[0].geojson):
            newLayer = LayerHistory(layer=self, name=self.name, type=self.type, geojson=self.geojson)
            newLayer.save()

    class Meta:
        app_label = 'qml'
        #unique_together = ('name', 'type',)

    def __str__(self):
        return f'{self.type}:{self.name}' if self.type else f'{self.name}'


class LayerHistory(LayerBase):
    """ From https://stackoverflow.com/questions/10540111/store-versioned-history-of-field-in-a-django-model """
    version = models.IntegerField(editable=False)
    layer = models.ForeignKey('Layer', on_delete=models.CASCADE, related_name='+')

    def save(self, *args, **kwargs):
        # start with version 1 and increment it for each book
        #current_version = LayerHistory.objects.filter(layer=self.layer).order_by('-version')[:1]
        current_version = LayerHistory.objects.filter(layer__name=self.layer.name, layer__type=self.layer.type).order_by('-version')[:1]
        self.version = current_version[0].version + 1 if current_version else 1
        super(LayerHistory, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.type}:{self.name}, verson: {self.version}' if self.type else f'{self.name}, verson: {self.version}'

    class Meta:
        app_label = 'qml'
        unique_together = ('version', 'layer',)

