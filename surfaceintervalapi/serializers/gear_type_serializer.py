from rest_framework import serializers
from surfaceintervalapi.models import Gear_Type


class GearTypeSerializer (serializers.ModelSerializer):

    class Meta:
        model = Gear_Type
        fields = ('id','name',)