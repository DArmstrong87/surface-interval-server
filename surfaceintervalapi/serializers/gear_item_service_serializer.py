from rest_framework import serializers

from surfaceintervalapi.models import GearItemService
from surfaceintervalapi.serializers.gear_item_serializer import GearItemSerializer


class GearItemServiceSerializer(serializers.ModelSerializer):
    gear_item = GearItemSerializer()

    class Meta:
        model = GearItemService
        fields = (
            "id",
            "gear_item",
            "service_date",
        )
        depth = 1
