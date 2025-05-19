from rest_framework import serializers

from surfaceintervalapi.models import GearItemServiceInterval


class GearItemServiceIntervalSerializer(serializers.ModelSerializer):
    class Meta:
        model = GearItemServiceInterval
        fields = (
            "id",
            "purchase_date",
            "dive_interval",
            "day_interval",
        )
        depth = 1
