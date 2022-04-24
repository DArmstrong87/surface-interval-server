from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from surfaceintervalapi.models import Gear_Type
from surfaceintervalapi.serializers import GearTypeSerializer


class GearTypeView(ViewSet):

    def list(self, request):
        gear_types = Gear_Type.objects.all()
        serializer = GearTypeSerializer(
            gear_types, many=True, context={'request': request})
        return Response(serializer.data)
