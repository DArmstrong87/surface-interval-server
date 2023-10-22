from rest_framework import serializers
from surfaceintervalapi.models import CustomSpecialty


class CustomSpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomSpecialty
        fields = (
            "id",
            "name",
        )
