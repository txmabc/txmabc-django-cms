from rest_framework import serializers
from manager.models import CategoryModel

class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = "__all__"