from rest_framework import serializers
from surfaceintervalapi.models import Specialty


class SpecialtySerializer (serializers.ModelSerializer):

    class Meta:
        model = Specialty
        fields = ('id','name')