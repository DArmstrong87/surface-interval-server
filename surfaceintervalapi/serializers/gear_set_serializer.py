from rest_framework import serializers
from surfaceintervalapi.models import GearSet


class GearSetSerializer(serializers.ModelSerializer):
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
