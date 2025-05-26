from rest_framework import serializers
from pytz import timezone as pytz_timezone
from typing import Optional

from surfaceintervalapi.models import GearItem
from surfaceintervalapi.serializers.custom_gear_type_serializer import CustomGearTypeSerializer
from surfaceintervalapi.serializers.gear_item_service_serializer import GearItemServiceSerializer
from surfaceintervalapi.serializers.gear_type_serializer import GearTypeSerializer
from surfaceintervalapi.serializers.gear_item_service_interval_serializer import (
    GearItemServiceIntervalSerializer,
)


class GearItemSerializer(serializers.ModelSerializer):
    gear_type = GearTypeSerializer()
    custom_gear_type = CustomGearTypeSerializer()
    service_history = GearItemServiceSerializer(many=True)
    service_interval = GearItemServiceIntervalSerializer()
    days_since_last_service = serializers.SerializerMethodField()
    due_for_service_days = serializers.SerializerMethodField()

    def _get_timezone(self):
        tz_name = self.context.get("timezone")
        if tz_name:
            try:
                return pytz_timezone(tz_name)
            except Exception:
                return None
        return None

    def get_days_since_last_service(self, instance) -> Optional[int]:
        tz = self._get_timezone()
        return instance.get_days_since_last_service(tz=tz)

    def get_due_for_service_days(self, instance) -> Optional[int]:
        tz = self._get_timezone()
        return instance.get_due_for_service_days(tz=tz)

    class Meta:
        model = GearItem
        fields = (
            "id",
            "gear_type",
            "custom_gear_type",
            "name",
            "service_tracking",
            "service_interval",
            "service_history",
            "last_service_date",
            "dives_since_last_service",
            "days_since_last_service",
            "due_for_service_days",
            "due_for_service_dives",
            "dive_count",
        )
        depth = 1


class GearItemSimpleSerializer(serializers.ModelSerializer):
    gear_type = GearTypeSerializer()
    custom_gear_type = CustomGearTypeSerializer()

    class Meta:
        model = GearItem
        fields = (
            "id",
            "gear_type",
            "custom_gear_type",
            "name",
            "service_tracking",
        )
        depth = 1
