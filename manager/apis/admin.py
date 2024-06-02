from django.shortcuts import render
from rest_framework import routers, serializers, viewsets

# Create your views here.
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from manager.models import Admin as AdminModel, AdminPart as AdminPartModel

# Serializers define the API representation.
class AdminSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AdminModel
        fields = '__all__'

# ViewSets define the view behavior.
class AdminViewSet(viewsets.ModelViewSet):
    queryset = AdminModel.objects.all()
    serializer_class = AdminSerializer

    def create(self, request, *args, **kwargs):
        _mutable = request.data._mutable
        request.data._mutable = True
        request.data['adminpass']=make_password(request.data['adminpass'])
        request.data._mutable = _mutable
        return super().create(request, *args, **kwargs)

# Serializers define the API representation.
class AdminPartSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AdminPartModel
        fields = '__all__'

# ViewSets define the view behavior.
class AdminPartViewSet(viewsets.ModelViewSet):
    queryset = AdminPartModel.objects.all()
    serializer_class = AdminPartSerializer

    def create(self, request, *args, **kwargs):
        print(request)
        return super().create(request, *args, **kwargs)
