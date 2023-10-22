from rest_framework import serializers
from surfaceintervalapi.models import GearType


class GearTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GearType
        fields = (
            "id",
            "name",
        )
