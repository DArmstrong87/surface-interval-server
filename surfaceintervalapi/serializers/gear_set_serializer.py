from rest_framework import serializers
from surfaceintervalapi.models import GearSet, GearItem, GearType, CustomGearType


class GearTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GearType
        fields = ("id", "name")


class CustomGearTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomGearType
        fields = ("id", "name")


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
            "dives_since_last_service",
            "days_since_last_service",
            "get_due_for_service_days",
            "due_for_service_dives",
        )
        depth = 1


class GearSetSerializer(serializers.ModelSerializer):
    gear_items = GearItemSerializer(many=True)

    class Meta:
        model = GearSet
        fields = (
            "id",
            "name",
            "gear_items",
            "weight",
        )
        depth = 1
