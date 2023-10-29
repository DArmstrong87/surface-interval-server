from rest_framework import serializers
from surfaceintervalapi.models import CertificationCard


class CertCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificationCard
        fields = ("id", "name", "date_issued", "image_front_url", "image_back_url")
