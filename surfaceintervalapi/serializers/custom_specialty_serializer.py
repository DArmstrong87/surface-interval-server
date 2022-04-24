from rest_framework import serializers
from surfaceintervalapi.models import Custom_Specialty


class CustomSpecialtySerializer (serializers.ModelSerializer):

    class Meta:
        model = Custom_Specialty
        fields = ('id','name',)