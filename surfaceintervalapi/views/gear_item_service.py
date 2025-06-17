from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from surfaceintervalapi.models import GearItem, GearItemService, GearItemServiceInterval
from surfaceintervalapi.serializers import GearItemServiceSerializer


class GearItemServiceView(ModelViewSet):
    queryset = GearItemService.objects.all()
    serializer_class = GearItemServiceSerializer

    def create(self, request):
        try:
            gear_item_id = request.data["gearItemId"]
            service_date = request.data["serviceDate"]
        except KeyError as ex:
            return Response(
                {"error": f"Missing required field: {ex.args[0]}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # See if this item is being tracked for service
        gear_item_service_interval_exists = GearItemServiceInterval.objects.filter(
            gear_item__id=gear_item_id, gear_item__diver__user=request.user
        ).exists()
        if not gear_item_service_interval_exists:
            return Response(
                {
                    "error": "GearItemServiceInterval with the provided ID does not exist. Service cannot be tracked."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            gear_item = GearItem.objects.get(pk=gear_item_id, diver__user=request.user)
            gear_item_service = GearItemService.objects.create(
                gear_item=gear_item,
                service_date=service_date,
            )
            serializer = self.serializer_class(
                gear_item_service, many=False, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except GearItem.DoesNotExist:
            return Response(
                {"error": "GearItem with the provided ID does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def destroy(self, request, pk=None):
        try:
            gear_item_service = GearItemService.objects.get(
                pk=pk, gear_item__diver__user=request.user
            )
            gear_item_service.delete()

            return Response({"GearItemService deleted"}, status=status.HTTP_204_NO_CONTENT)

        except GearItemService.DoesNotExist as ex:
            return Response({"error": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({"error": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        try:
            gear_item_id = request.query_params.get("gearItemId")
            if gear_item_id:
                gear_item_services = GearItemService.objects.filter(
                    gear_item__id=gear_item_id, gear_item__diver__user=request.user
                ).order_by("-service_date")
            else:
                return Response(
                    {"error": "gearItemId is required"}, status=status.HTTP_400_BAD_REQUEST
                )

            serializer = self.serializer_class(
                gear_item_services, many=True, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        except GearItemService.DoesNotExist as ex:
            return Response({"error": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
