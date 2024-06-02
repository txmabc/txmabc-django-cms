from django.shortcuts import render
from rest_framework import routers, serializers, viewsets

# Create your views here.
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from manager.models import UserGroupModel

# Serializers define the API representation.
class UserGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserGroupModel
        fields = '__all__'

# ViewSets define the view behavior.
class UserGroupViewSet(viewsets.ModelViewSet):
    queryset = UserGroupModel.objects.all()
    serializer_class = UserGroupSerializer