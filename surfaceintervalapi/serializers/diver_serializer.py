from django.contrib.auth import get_user_model
from rest_framework import serializers

from surfaceintervalapi.models import Diver


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "username")


class DiverSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Diver
        fields = (
            "id",
            "user",
            "units",
            "total_dives",
            "most_recent_dive",
            "deepest_dive",
            "longest_dive",
            "shortest_dive",
            "most_logged_specialty",
            "avg_air_consumption",
            "most_logged_specialty",
        )
        depth = 1
