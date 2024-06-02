from django.shortcuts import render
from rest_framework import routers, serializers, viewsets

# Create your views here.
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from manager.models import CategoryModel

# Serializers define the API representation.
class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CategoryModel
        fields = '__all__'

# ViewSets define the view behavior.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = CategoryModel.objects.all()
    serializer_class = CategorySerializer