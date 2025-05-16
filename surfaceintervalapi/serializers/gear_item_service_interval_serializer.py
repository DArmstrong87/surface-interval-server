from rest_framework import serializers

from surfaceintervalapi.models import GearItemServiceInterval
from surfaceintervalapi.serializers.gear_item_serializer import GearItemSerializer


class GearItemServiceIntervalSerializer(serializers.ModelSerializer):
    gear_item = GearItemSerializer()

    class Meta:
        model = GearItemServiceInterval
        fields = (
            "id",
            "gear_item",
            "purchase_date",
            "dive_interval",
            "day_interval",
        )
        depth = 1
