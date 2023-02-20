from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','first_name','last_name','email']

class FigerSerializer(serializers.Serializer):
    image = serializers.FileField()
    class Meta:
        fields = ['image']
