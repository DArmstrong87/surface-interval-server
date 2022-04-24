from rest_framework import serializers
from surfaceintervalapi.models import Certification_Card


class CertCardSerializer (serializers.ModelSerializer):

    class Meta:
        model = Certification_Card
        fields = ('id', 'name', 'date_issued', 'image_front_url', 'image_back_url')