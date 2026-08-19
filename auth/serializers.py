from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterSerializer (serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','password']
        extra_kwargs = {'email': {'required': True , 'allow_blank' : False}}



class LoginSerializer (serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

