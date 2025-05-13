from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from surfaceintervalapi.models import GearType
from surfaceintervalapi.serializers import GearTypeSerializer


class GearTypeView(ModelViewSet):
    queryset = GearType.objects.all()
    serializer_class = GearTypeSerializer

    def list(self, request):
        gear_types = GearType.objects.all()
        serializer = GearTypeSerializer(gear_types, many=True, context={"request": request})
        return Response(serializer.data)
