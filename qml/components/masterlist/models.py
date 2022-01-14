#from django.db import models
from django.contrib.gis.db import models

# Next lin needed, to migrate ledger_api_clinet module
from ledger_api_client.ledger_models import EmailUserRO as EmailUser



class DpawRegion(models.Model):
    feat_id = models.CharField(max_length=64)
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


#class Question1(models.Model):
#    question_text = models.CharField(max_length=200)
#    pub_date = models.DateTimeField('date published')
#
#    class Meta:
#        app_label = 'qml'
