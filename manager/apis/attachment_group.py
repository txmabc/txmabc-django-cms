from django.shortcuts import render
from rest_framework import routers, serializers, viewsets

# Create your views here.
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from manager.models import AttachmentGroup as AttachmentGroupModel

# Serializers define the API representation.
class AttachmentGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AttachmentGroupModel
        fields = '__all__'

# ViewSets define the view behavior.
class AttachmentGroupViewSet(viewsets.ModelViewSet):
    queryset = AttachmentGroupModel.objects.all()
    serializer_class = AttachmentGroupSerializer