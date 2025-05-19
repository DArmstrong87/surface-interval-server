from rest_framework import serializers

from surfaceintervalapi.models import GearItemService


class GearItemServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GearItemService
        fields = (
            "id",
            "gear_item",
            "service_date",
        )
