from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from surfaceintervalapi.models import Diver, CustomSpecialty
from surfaceintervalapi.serializers import CustomSpecialtySerializer
from surfaceintervalapi.types import CACHE_TIME_MINS
from surfaceintervalapi.utils import cache_values, get_values_from_cache


class CustomSpecialtyView(ModelViewSet):
    queryset = CustomSpecialty.objects.all()
    serializer_class = CustomSpecialtySerializer

    def retrieve(self, request, pk):
        cache_key = f"user:{request.user.id}:custom_specialty:{pk}"
        cached_custom_specialty = get_values_from_cache(cache_key)
        if cached_custom_specialty:
            return Response(cached_custom_specialty, status=status.HTTP_200_OK)

        custom_specialty = CustomSpecialty.objects.get(pk=pk, diver__user=request.user)
        serializer = CustomSpecialtySerializer(
            custom_specialty, many=True, context={"request": request}
        )
        cache_values(cache_key, serializer.data, CACHE_TIME_MINS)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        cache_key = f"user:{request.user.id}:custom_specialties"
        cached_custom_specialties = get_values_from_cache(cache_key)
        if cached_custom_specialties:
            return Response(cached_custom_specialties, status=status.HTTP_200_OK)
        custom_specialty = CustomSpecialty.objects.filter(diver__user=request.user)
        serializer = CustomSpecialtySerializer(
            custom_specialty, many=True, context={"request": request}
        )
        cache_values(cache_key, serializer.data, CACHE_TIME_MINS)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        diver = Diver.objects.get(user=request.user)

        try:
            custom_specialty = CustomSpecialty.objects.create(
                diver=diver,
                name=request.data["name"],
            )

            serializer = CustomSpecialtySerializer(
                custom_specialty, many=False, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as ex:
            return Response({"error": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        diver = Diver.objects.get(user=request.user)

        try:
            custom_specialty = CustomSpecialty.objects.get(pk=pk, diver=diver)
            custom_specialty.delete()

            return Response({"CustomSpecialty deleted"}, status=status.HTTP_204_NO_CONTENT)

        except CustomSpecialty.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk):
        diver = Diver.objects.get(user=request.user)

        try:
            custom_specialty = CustomSpecialty.objects.get(diver=diver, pk=pk)
            custom_specialty.name = request.data["name"]

            custom_specialty.save()

            serializer = CustomSpecialtySerializer(
                custom_specialty, many=False, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

        except Exception as ex:
            return Response({"error": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
