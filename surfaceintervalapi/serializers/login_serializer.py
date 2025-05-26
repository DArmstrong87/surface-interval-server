# serializers.py
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class TokenSerializer(serializers.Serializer):
    valid = serializers.BooleanField()
    token = serializers.CharField()
    refresh = serializers.CharField()
