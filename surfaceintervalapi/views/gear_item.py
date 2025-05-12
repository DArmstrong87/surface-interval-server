from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from surfaceintervalapi.models import Diver, GearItem, CustomGearType, GearType
from surfaceintervalapi.serializers import GearItemSerializer


class GearItemView(ModelViewSet):
    queryset = GearItem.objects.all()
    serializer_class = GearItemSerializer

    def retrieve(self, request, pk):
        gear_item = GearItem.objects.get(pk=pk, diver__user=request.auth.user)
        serializer = GearItemSerializer(gear_item, many=False, context={"request": request})
        return Response(serializer.data)

    def list(self, request):
        gear_items = GearItem.objects.filter(diver__user=request.auth.user)
        serializer = GearItemSerializer(gear_items, many=True, context={"request": request})
        return Response(serializer.data)

    def create(self, request):
        diver = Diver.objects.get(user=request.auth.user)
        try:
            gear_type = GearType.objects.get(pk=request.data["gear_type"])
            custom_gear_type = None
        except:
            custom_gear_type = CustomGearType.objects.get(pk=request.data["custom_gear_type"])
            gear_type = None

        try:
            gear_item = GearItem.objects.create(
                diver=diver,
                name=request.data["name"],
                gear_type=gear_type,
                custom_gear_type=custom_gear_type,
                purchase_date=request.data["purchase_date"],
                last_serviced=request.data["last_serviced"],
            )

            serializer = GearItemSerializer(gear_item, many=False, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as ex:
            return Response({"error": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, pk):
        try:
            diver = (Diver.objects.get(user=request.auth.user),)
            gear_item = GearItem.objects.get(pk=pk, diver=diver)

            gear_item.name = (request.data["name"],)
            gear_item.gear_type = (request.data["gear_type"],)
            gear_item.custom_gear_type = (request.data["custom_gear_type"],)
            gear_item.purchase_date = (request.data["purchase_date"],)
            gear_item.last_serviced = request.data["last_serviced"]
            gear_item.save()

            serializer = GearItemSerializer(gear_item, many=False, context={"request": request})
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

        except Exception as ex:
            return Response({"error": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            gear_item = GearItem.objects.get(pk=pk, diver__user=request.auth.user)
            gear_item.delete()

            return Response({"GearItem deleted"}, status=status.HTTP_204_NO_CONTENT)

        except GearItem.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
