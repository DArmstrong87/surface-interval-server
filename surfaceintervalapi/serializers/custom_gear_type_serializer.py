from rest_framework import serializers
from surfaceintervalapi.models import Custom_Gear_Type


class CustomGearTypeSerializer (serializers.ModelSerializer):

    class Meta:
        model = Custom_Gear_Type
        fields = ('id','name',)