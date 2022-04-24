from rest_framework import serializers

from surfaceintervalapi.models import Dive, Favorite_Dive
from surfaceintervalapi.serializers.diver_serializer import DiverSerializer

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
                'air_consumption',
                'favorite'
                )
        
class FavoriteDiveSerializer (serializers.ModelSerializer):
    dive = DiveSerializer()
    diver = DiverSerializer

    class Meta:
        model = Favorite_Dive
        fields = ('id', 'dive', 'diver')