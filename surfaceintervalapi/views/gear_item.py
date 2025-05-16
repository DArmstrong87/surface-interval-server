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
        try:
            diver = Diver.objects.get(user=request.auth.user)
            gear_type_id = request.data["gearTypeId"]
            custom_gear_type_id = request.data["customGearTypeId"]
            new_custom_gear_type = request.data["newCustomGearType"]
            item_name = request.data["name"]
        except Diver.DoesNotExist:
            return Response(
                {"error": f"Diver of ID {request.auth.user.id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except KeyError:
            return Response(
                {
                    "error": "Request must contain name, gearTypeId, customGearTypeId and newCustomGearType"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        use_gear_type = (
            gear_type_id is not None
            and custom_gear_type_id is None
            and (new_custom_gear_type is None or new_custom_gear_type == "")
        )
        use_custom_gear_type = (
            gear_type_id is None
            and custom_gear_type_id is not None
            and (new_custom_gear_type is None or new_custom_gear_type == "")
        )
        create_new_custom_gear_type = (
            gear_type_id is None
            and custom_gear_type_id is None
            and (new_custom_gear_type is not None and new_custom_gear_type != "")
        )

        gear_type = None
        custom_gear_type = None

        if use_gear_type:
            try:
                gear_type = GearType.objects.get(pk=request.data["gearTypeId"])
            except GearType.DoesNotExist:
                return Response(
                    {"error": f"GearType of ID {gear_type_id} not found."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        elif use_custom_gear_type:
            try:
                custom_gear_type = CustomGearType.objects.get(pk=custom_gear_type_id)
            except CustomGearType.DoesNotExist:
                return Response(
                    {"error": "Custom GearType not found."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        elif create_new_custom_gear_type:
            custom_gear_type = CustomGearType.objects.create(diver=diver, name=new_custom_gear_type)
        else:
            return Response(
                {
                    "error": "Conflicting data on whether to use existing GearType, Custom GearType or create new Custom GearType. Ensure only 1 is not null."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            gear_item = GearItem.objects.create(
                diver=diver,
                name=item_name,
                gear_type=gear_type,
                custom_gear_type=custom_gear_type,
            )

            serializer = GearItemSerializer(gear_item, many=False, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as ex:
            return Response({"error": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk):
        try:
            name = request.data["name"]
            gear_type_id = request.data["gearTypeId"]
            custom_gear_type_id = request.data["customGearTypeId"]
        except KeyError:
            return Response(
                {
                    "error": "Request must contain name, gearTypeId, customGearTypeId and newCustomGearType"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            if gear_type_id is not None:
                gear_type = GearType.objects.get(pk=gear_type_id)
            else:
                gear_type = None

            if custom_gear_type_id is not None:
                custom_gear_type = CustomGearType.objects.get(
                    pk=custom_gear_type_id, diver__user=request.auth.user
                )
            else:
                custom_gear_type = None
        except GearType.DoesNotExist:
            return Response(
                {"error": f"GearType of ID {gear_type_id} not found."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except CustomGearType.DoesNotExist:
            return Response(
                {"error": f"CustomGearType of ID {custom_gear_type_id} not found."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            diver = Diver.objects.get(user=request.auth.user)
            gear_item = GearItem.objects.get(pk=pk, diver=diver)

            gear_item.name = name
            gear_item.gear_type = gear_type
            gear_item.custom_gear_type = custom_gear_type
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
