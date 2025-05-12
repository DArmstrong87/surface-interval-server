# serializers.py
from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    first_name = (serializers.CharField(),)
    last_name = (serializers.CharField(),)
    units = serializers.CharField()


class RegisterTokenSerializer(serializers.Serializer):
    token = serializers.CharField()
