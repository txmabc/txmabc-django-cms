from rest_framework import serializers
from manager.models import UserModel

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = "__all__"