from rest_framework import serializers

from surfaceintervalapi.models import Dive, FavoriteDive
from surfaceintervalapi.serializers.diver_serializer import DiverSerializer


class DiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dive
        fields = (
            "id",
            "date",
            "gear_set",
            "location",
            "site",
            "water",
            "depth",
            "time",
            "description",
            "start_pressure",
            "end_pressure",
            "tank_vol",
            "air_consumption",
            "favorite",
            "specialties",
        )


class FavoriteDiveSerializer(serializers.ModelSerializer):
    dive = DiveSerializer()
    diver = DiverSerializer

    class Meta:
        model = FavoriteDive
        fields = ("id", "dive", "diver")
