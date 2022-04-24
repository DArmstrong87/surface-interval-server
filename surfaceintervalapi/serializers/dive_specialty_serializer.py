from rest_framework import serializers
from surfaceintervalapi.models import Dive_Specialty


class DiveSpecialtySerializer (serializers.ModelSerializer):

    class Meta:
        model = Dive_Specialty
        fields = ('id','name',)