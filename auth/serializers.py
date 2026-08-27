from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterSerializer (serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','password']
        extra_kwargs = {'email': {'required': True , 'allow_blank' : False}}

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value



class LoginSerializer (serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

