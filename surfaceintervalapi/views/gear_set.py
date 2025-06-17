from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from surfaceintervalapi.models import Diver, GearSet, GearItem
from surfaceintervalapi.serializers import GearSetSerializer
from surfaceintervalapi.utils import cache_values, get_values_from_cache


class GearSetView(ModelViewSet):
    queryset = GearSet.objects.all()
    serializer_class = GearSetSerializer

    def retrieve(self, request, pk):
        try:
            cache_key = f"user:{request.user.id}:gear_set:{pk}"
            cached_gear_set = get_values_from_cache(cache_key)
            if cached_gear_set:
                return Response(cached_gear_set, status=status.HTTP_200_OK)

            gear_set = GearSet.objects.get(pk=pk, diver__user=request.user)
            serializer = GearSetSerializer(gear_set, many=False, context={"request": request})
            cache_values(cache_key, gear_set, 10)
            return Response(serializer.data)
        except GearSet.DoesNotExist:
            return Response(
                {"error": "GearSet matching query does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

    def list(self, request):
        try:
            cache_key = f"user:{request.user.id}:gear_sets"
            cached_gear_sets = get_values_from_cache(cache_key)
            if cached_gear_sets:
                return Response(cached_gear_sets, status=status.HTTP_200_OK)

            gear_sets = GearSet.objects.filter(diver__user=request.user)
            serializer = GearSetSerializer(gear_sets, many=True, context={"request": request})
            cache_values(cache_key, serializer.data, 10)
            return Response(serializer.data)
        except Exception as ex:
            return Response(
                {"error": f"An error occurred while retrieving gear sets: {str(ex)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def create(self, request):
        try:
            name = request.data["name"]
            gear_items = request.data["gearItemIds"]
            weight = request.data["weight"]
        except KeyError as ex:
            return Response(
                {"error": f"Missing required fields: {str(ex)}"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            diver = Diver.objects.get(user=request.user)

            # Verify all gear items exist and belong to the user
            gear_items_queryset = GearItem.objects.filter(
                id__in=gear_items, diver__user=request.user
            )
            if len(gear_items_queryset) != len(gear_items):
                return Response(
                    {"error": "One or more gear items not found"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            gear_set = GearSet.objects.create(diver=diver, name=name, weight=weight)
            gear_set.gear_items.set(gear_items_queryset)
            gear_set.save()

            serializer = GearSetSerializer(gear_set, many=False, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as ex:
            return Response({"error": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk):
        try:
            name = request.data["name"]
            gear_items = request.data["gearItemIds"]
            weight = request.data["weight"]
        except KeyError as ex:
            return Response(
                {"error": f"Missing required fields: {str(ex)}"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Verify all gear items exist and belong to the user
        gear_items_queryset = GearItem.objects.filter(id__in=gear_items, diver__user=request.user)
        if len(gear_items_queryset) != len(gear_items):
            return Response(
                {"error": "One or more gear items not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            gear_set = GearSet.objects.get(pk=pk, diver__user=request.user)
            gear_set.name = name
            gear_set.weight = weight
            gear_set.gear_items.set(gear_items_queryset)
            gear_set.save()

            return Response({"message": "Gear set updated!"}, status=status.HTTP_204_NO_CONTENT)

        except GearSet.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            gear_set = GearSet.objects.get(pk=pk, diver__user=request.user)
            gear_set.delete()

            return Response({"GearSet deleted"}, status=status.HTTP_204_NO_CONTENT)

        except GearSet.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
