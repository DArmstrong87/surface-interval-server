from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from surfaceintervalapi.models import GearItem, GearItemServiceInterval
from surfaceintervalapi.serializers import GearItemServiceSerializer


class GearItemVServiceIntervalView(ModelViewSet):
    queryset = GearItemServiceInterval.objects.all()
    serializer_class = GearItemServiceSerializer

    def create(self, request):
        gear_item_id = request.data.get("gearItemId")

        try:
            gear_item_service_interval = GearItemServiceInterval.objects.create(
                gear_item=GearItem.objects.get(pk=gear_item_id),
                purchase_date=request.data["purchaseDate"],
                dives=request.data["dives"],
                days=request.data["days"],
            )
            serializer = self.serializer_class(
                gear_item_service_interval, many=False, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except GearItem.DoesNotExist:
            return Response(
                {"error": "GearItem with the provided ID does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except KeyError as ex:
            return Response(
                {"error": f"Missing required field: {ex.args[0]}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def destroy(self, request, pk=None):
        try:
            gear_item = GearItemServiceInterval.objects.get(
                pk=pk, gear_item__diver__user=request.auth.user
            )
            gear_item.delete()

            return Response({"GearItemServiceInterval deleted"}, status=status.HTTP_204_NO_CONTENT)

        except GearItemServiceInterval.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
