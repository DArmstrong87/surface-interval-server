from rest_framework import serializers
from surfaceintervalapi.models import GearSet
from surfaceintervalapi.serializers.gear_item_serializer import GearItemSerializer


class GearSetSerializer(serializers.ModelSerializer):
    bcd = GearItemSerializer()
    regulator = GearItemSerializer()
    octopus = GearItemSerializer()
    mask = GearItemSerializer()
    fins = GearItemSerializer()
    boots = GearItemSerializer()
    computer = GearItemSerializer()
    exposure_suit = GearItemSerializer()
    tank = GearItemSerializer()

    class Meta:
        model = GearSet
        fields = (
            "id",
            "name",
            "bcd",
            "regulator",
            "octopus",
            "mask",
            "fins",
            "boots",
            "computer",
            "exposure_suit",
            "weights",
            "tank",
        )
        depth = 1
