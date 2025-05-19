from rest_framework import serializers
from surfaceintervalapi.models import GearSet, GearType, CustomGearType
from surfaceintervalapi.serializers import GearItemSimpleSerializer


class GearTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GearType
        fields = ("id", "name")


class CustomGearTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomGearType
        fields = ("id", "name")


class GearSetSerializer(serializers.ModelSerializer):
    gear_items = GearItemSimpleSerializer(many=True)

    class Meta:
        model = GearSet
        fields = (
            "id",
            "name",
            "gear_items",
            "weight",
        )
