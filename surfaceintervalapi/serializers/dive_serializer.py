from rest_framework import serializers
from surfaceintervalapi.models import Dive


class DiveSerializer (serializers.ModelSerializer):

    class Meta:
        model = Dive
        fields = ('id',
                'date',
                'gear_set',
                'country_state',
                'site',
                'water',
                'depth',
                'time',
                'description',
                'start_pressure',
                'end_pressure',
                'tank_vol',
                'air_consumption'
                )