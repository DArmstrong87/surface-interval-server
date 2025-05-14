from rest_framework import serializers

from surfaceintervalapi.models import GearItem
from surfaceintervalapi.serializers.custom_gear_type_serializer import CustomGearTypeSerializer
from surfaceintervalapi.serializers.gear_type_serializer import GearTypeSerializer


class GearItemSerializer(serializers.ModelSerializer):
    gear_type = GearTypeSerializer()
    custom_gear_type = CustomGearTypeSerializer()

    class Meta:
        model = GearItem
        fields = (
            "id",
            "gear_type",
            "custom_gear_type",
            "name",
        )
        depth = 1
