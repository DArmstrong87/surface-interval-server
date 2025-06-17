from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from surfaceintervalapi.models import GearType
from surfaceintervalapi.serializers import GearTypeSerializer
from surfaceintervalapi.types import CACHE_TIME_MINS
from surfaceintervalapi.utils import cache_values, get_values_from_cache


class GearTypeView(ModelViewSet):
    queryset = GearType.objects.all()
    serializer_class = GearTypeSerializer

    def list(self, request):
        cache_key = "gear_types"
        cached_gear_types = get_values_from_cache(cache_key)
        if cached_gear_types:
            return Response(cached_gear_types, status=status.HTTP_200_OK)

        gear_types = GearType.objects.all()
        serializer = GearTypeSerializer(gear_types, many=True, context={"request": request})
        cache_values(cache_key, serializer.data, CACHE_TIME_MINS)
        return Response(serializer.data)
