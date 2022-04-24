from rest_framework import serializers
from surfaceintervalapi.models import Gear_Set


class GearSetSerializer (serializers.ModelSerializer):
    

    class Meta:
        model = Gear_Set
        fields = ('id',
                  'name',
                  'bcd',
                  'regulator',
                  'octopus',
                  'mask',
                  'fins',
                  'boots',
                  'computer',
                  'exposure_suit',
                  'weights',
                  'tank'
                  )
        depth = 1
        
