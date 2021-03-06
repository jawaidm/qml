from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.db import transaction
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.db.models import Q

from wsgiref.util import FileWrapper
from rest_framework import viewsets, serializers, status, generics, views
#from rest_framework.decorators import detail_route, list_route, renderer_classes, parser_classes
from rest_framework.decorators import action, renderer_classes, parser_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, BasePermission
from rest_framework.pagination import PageNumberPagination
import traceback
import json

from qml.components.masterlist.models import Layer, LayerHistory, Feature
from qml.utils.geoquery_utils import GeoQueryHelper
from qml.components.masterlist.serializers import GeoTestSerializer, LayerSerializer, FeatureGeometrySerializer

import logging
#logger = logging.getLogger('payment_checkout')
logger = logging.getLogger(__name__)


#class _GeoTestViewSet(viewsets.ReadOnlyModelViewSet):
#    queryset = Layer.objects.all().order_by('id')
#    serializer_class = GeoTestSerializer
#
#    @detail_route(methods=['GET',])
#    def layers(self, request, *args, **kwargs):            
#        instance = self.get_object()
#        qs = instance.land_parks
#        qs.order_by('id')
#        serializer = ParkSerializer(qs,context={'request':request}, many=True)
#        return Response(serializer.data)
#
#    @detail_route(methods=['GET',])
#    def parks(self, request, *args, **kwargs):            
#        instance = self.get_object()
#        qs = instance.parks
#        qs.order_by('id')
#        serializer = ParkSerializer(qs,context={'request':request}, many=True)
#        return Response(serializer.data)


class LayerViewSet(viewsets.ReadOnlyModelViewSet):
    """ http://localhost:8002/api/layers.json """
    queryset = Layer.objects.filter(current=True).order_by('id')
    serializer_class = LayerSerializer

    @action(detail=True, methods=['GET',])
    def layer(self, request, *args, **kwargs):            
        """ http://localhost:8002/api/layers/50/layer.json """
        instance = self.get_object()
        serializer = self.get_serializer(instance) 
        return Response(serializer.data)


class FeatureViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Layer.objects.all().order_by('id')
    serializer_class = LayerSerializer

    @action(detail=True, methods=['GET',])
    def features(self, request, *args, **kwargs):            
        """ http://localhost:8002/api/layer_features/50/features.json """
        #import ipdb; ipdb.set_trace()
        instance = self.get_object()
        qs = instance.feature_features.all()
        qs.order_by('id')
        serializer = FeatureGeometrySerializer(qs,context={'request':request}, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['POST',])
    def intersect(self, request, *args, **kwargs):            
        """ 
        http://localhost:8002/api/layer_features/50/intersect.json 

        curl -d @qml/data/json/goldfields_curl_query.json -X POST http://localhost:8002/api/layer_features/50/intersect.json --header "Content-Type: application/json" --header "Accept: application/json"
        """
        #import ipdb; ipdb.set_trace()
        names = request.data['names']
        geojson = request.data['geojson']
        layer = self.get_object()


        helper=GeoQueryHelper(layer)
        #res = helper.intersection(['region', 'office'], request.data)
        res = helper.intersection(names, geojson)
        return Response(res)



#    @detail_route(methods=['GET',])
#    def internal_proposal(self, request, *args, **kwargs):
#        instance = self.get_object()
#        serializer = InternalProposalSerializer(instance,context={'request':request})
#        if instance.application_type.name==ApplicationType.TCLASS:
#            serializer = InternalProposalSerializer(instance,context={'request':request})
#        elif instance.application_type.name==ApplicationType.FILMING:
#            serializer = InternalFilmingProposalSerializer(instance,context={'request':request})
#        elif instance.application_type.name==ApplicationType.EVENT:
#            serializer = InternalEventProposalSerializer(instance,context={'request':request})
#        return Response(serializer.data)

