from rest_framework import serializers
from manager.models import ContentModel

class LoginSerializers(serializers.Serializer):
    adminname = serializers.CharField(max_length=50)
    adminpass = serializers.CharField(max_length=50)


class ContentSerializers(serializers.ModelSerializer):
    class Meta:
        model = ContentModel
        fields = "__all__"