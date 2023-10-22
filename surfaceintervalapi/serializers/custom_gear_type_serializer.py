from rest_framework import serializers
from surfaceintervalapi.models import CustomGearType


class CustomGearTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomGearType
        fields = (
            "id",
            "name",
        )
