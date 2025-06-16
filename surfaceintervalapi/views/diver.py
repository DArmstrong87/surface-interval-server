from django.http import HttpResponseServerError

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from surfaceintervalapi.models import Diver
from surfaceintervalapi.serializers import DiverSerializer
from surfaceintervalapi.utils import cache_values, get_values_from_cache


class DiverView(ModelViewSet):
    queryset = Diver.objects.all()
    serializer_class = DiverSerializer

    def list(self, request):
        try:
            cache_key = f"user:{request.user.id}:diver"
            cached_diver = get_values_from_cache(cache_key)
            if cached_diver:
                return Response(cached_diver, status=status.HTTP_200_OK)
            diver = Diver.objects.get(user=request.user)
            serializer = DiverSerializer(diver, context={"request": request})
            cache_values(cache_key, serializer.data, 10)
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def retrieve(self, request, pk=None):
        try:
            cache_key = f"user:{request.user.id}:diver:{pk}"
            cached_diver = get_values_from_cache(cache_key)
            if cached_diver:
                return Response(cached_diver, status=status.HTTP_200_OK)

            diver = Diver.objects.get(pk=pk, user=request.user)
            serializer = DiverSerializer(diver, context={"request": request})
            cache_values(cache_key, serializer.data, 10)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Diver.DoesNotExist:
            return Response(f"Diver {pk} does not exist.", status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, pk):
        try:
            diver = Diver.objects.get(user=request.user)
            user = request.user

            diver.units = request.data["units"]
            user.first_name = request.data["first_name"]
            user.last_name = request.data["last_name"]

            user.save()
            diver.save()

            serializer = DiverSerializer(diver, many=False, context={"request": request})
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

        except Exception as ex:
            return Response({"error": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
