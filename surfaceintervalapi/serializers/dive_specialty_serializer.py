from rest_framework import serializers
from surfaceintervalapi.models import DiveSpecialty


class DiveSpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = DiveSpecialty
        fields = (
            "id",
            "name",
        )
