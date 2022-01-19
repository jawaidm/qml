from django.core.management.base import BaseCommand
from django.conf import settings
import subprocess
import os
from qml.utils.loader_utils import LayerLoader, layer_changed
from qml.components.masterlist.models import Layer, LayerHistory, Feature


import logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    """
    Load Layer util
    """

    help = 'Load Layer util: ./manage.py layer_loader cddp:dpaw_regions'
    #log_file = os.getcwd() + '/logs/layer_loader.log'

    def add_arguments(self, parser):
        parser.add_argument('name', nargs='?', type=str, default='cddp:dpaw_regions')

    def handle(self, *args, **options):
        name = options['name']
        layer_loader = LayerLoader(name=name)
        layer_loader.load_layer()

        for l in LayerHistory.objects.all():
            print(l.id, l, l.layer.feature_features.count(), l.layer.feature_features.values_list('id', flat=True))


