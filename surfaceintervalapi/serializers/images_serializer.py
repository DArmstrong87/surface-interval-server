from rest_framework import serializers

from surfaceintervalapi.models import Image
from surfaceintervalapi.serializers import DiveSerializer


class ImageSerializer(serializers.ModelSerializer):
    dive = DiveSerializer()

    class Meta:
        model = Image
        fields = ("id", "dive", "url")
