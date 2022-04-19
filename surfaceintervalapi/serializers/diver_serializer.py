from django.contrib.auth import get_user_model
from rest_framework import serializers

from surfaceintervalapi.models import Dive, Diver


class UserSerializer (serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username')
        
    
class DiverSerializer (serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Diver
        fields = ('id',
                  'user',
                  'units')
        depth=1