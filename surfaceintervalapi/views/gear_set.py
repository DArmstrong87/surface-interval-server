from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from surfaceintervalapi.models import Diver, GearSet
from surfaceintervalapi.serializers import GearSetSerializer


class GearSetView(ModelViewSet):
    queryset = GearSet.objects.all()
    serializer_class = GearSetSerializer

    def retrieve(self, request, pk):
        gear_set = GearSet.objects.get(pk=pk, diver__user=request.auth.user)
        serializer = GearSetSerializer(gear_set, many=False, context={"request": request})
        return Response(serializer.data)

    def list(self, request):
        gear_sets = GearSet.objects.filter(diver__user=request.auth.user)
        serializer = GearSetSerializer(gear_sets, many=True, context={"request": request})
        return Response(serializer.data)

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
            diver = Diver.objects.get(user=request.auth.user)
            gear_set = GearSet.objects.create(diver=diver, name=name, weight=weight)
            gear_set.gear_items.set(gear_items)
            gear_set.save()

            serializer = GearSetSerializer(gear_set, many=False, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as ex:
            return Response({"error": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk):
        try:
            name = request.data["name"]
            gear_items = request.data["gearItemIds"]
            weight = request.data["weight"]
        except KeyError as ex:
            return Response(
                {"error": f"Missing required fields: {str(ex)}"}, status=status.HTTP_400_BAD_REQUEST
            )

        gear_set = GearSet.objects.get(pk=pk, diver__user=request.auth.user)
        gear_set.name = name
        gear_set.weight = weight
        gear_set.gear_items.set(gear_items)
        gear_set.save()

        return Response({"message": "Gear set updated!"}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        try:
            gear_set = GearSet.objects.get(pk=pk, diver__user=request.auth.user)
            gear_set.delete()

            return Response({"GearSet deleted"}, status=status.HTTP_204_NO_CONTENT)

        except GearSet.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
