from django.shortcuts import render
from rest_framework import routers, serializers, viewsets

# Create your views here.
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from manager.models import Attachment as AttachmentModel

# Serializers define the API representation.
class AttachmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AttachmentModel
        fields = '__all__'

# ViewSets define the view behavior.
class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = AttachmentModel.objects.all()
    serializer_class = AttachmentSerializer