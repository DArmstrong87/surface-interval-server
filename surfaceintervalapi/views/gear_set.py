from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from surfaceintervalapi.models import Diver, Gear_Set, Gear_Set, Gear_Item
from surfaceintervalapi.serializers import GearSetSerializer


class GearSetView(ViewSet):

    def retrieve(self, request, pk):
        gear_set = Gear_Set.objects.get(pk=pk, diver__user=request.auth.user)
        serializer = GearSetSerializer(
            gear_set, many=False, context={'request': request})
        return Response(serializer.data)


    def list(self, request):
        gear_sets = Gear_Set.objects.filter(diver__user=request.auth.user)
        serializer = GearSetSerializer(
            gear_sets, many=True, context={'request': request})
        return Response(serializer.data)


    def create(self, request):
        diver = Diver.objects.get(user=request.auth.user)
        bcd = Gear_Item.objects.get(
            pk=request.data['bcd']) if 'bcd' in request.data else None
        regulator = Gear_Item.objects.get(
            pk=request.data['regulator']) if 'regulator' in request.data else None
        octopus = Gear_Item.objects.get(
            pk=request.data['octopus']) if 'octopus' in request.data else None
        mask = Gear_Item.objects.get(
            pk=request.data['mask']) if 'mask' in request.data else None
        fins = Gear_Item.objects.get(
            pk=request.data['fins']) if 'fins' in request.data else None
        boots = Gear_Item.objects.get(
            pk=request.data['boots']) if 'bootd' in request.data else None
        computer = Gear_Item.objects.get(
            pk=request.data['computer']) if 'computer' in request.data else None
        exposure_suit = Gear_Item.objects.get(
            pk=request.data['exposure_suit']) if 'exposure_suit' in request.data else None
        weights = request.data['weights'] if 'weights' in request.data else None
        tank = Gear_Item.objects.get(pk=request.data['tank']) if 'tank' in request.data else None

        try:
            gear_set = Gear_Set.objects.create(
                diver=diver,
                name=request.data['name'],
                bcd=bcd,
                regulator=regulator,
                octopus=octopus,
                mask=mask,
                fins=fins,
                boots=boots,
                computer=computer,
                exposure_suit=exposure_suit,
                weights=weights,
                tank=tank
            )

            serializer = GearSetSerializer(
                gear_set, many=False, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as ex:
            return Response({'error': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def partial_update(self, request, pk):
        try:
            gear_set = Gear_Set.objects.get(
                pk=pk, diver__user=request.auth.user)
            bcd = Gear_Item.objects.get(
                pk=request.data['bcd']) if 'bcd' in request.data else None
            regulator = Gear_Item.objects.get(
                pk=request.data['regulator']) if 'regulator' in request.data else None
            octopus = Gear_Item.objects.get(
                pk=request.data['octopus']) if 'octopus' in request.data else None
            mask = Gear_Item.objects.get(
                pk=request.data['mask']) if 'mask' in request.data else None
            fins = Gear_Item.objects.get(
                pk=request.data['fins']) if 'fins' in request.data else None
            boots = Gear_Item.objects.get(
                pk=request.data['boots']) if 'bootd' in request.data else None
            computer = Gear_Item.objects.get(
                pk=request.data['computer']) if 'computer' in request.data else None
            exposure_suit = Gear_Item.objects.get(
                pk=request.data['exposure_suit']) if 'exposure_suit' in request.data else None
            tank = Gear_Item.objects.get(
                pk=request.data['tank']) if 'tank' in request.data else None
            weights = request.data['weights'] if 'weights' in request.data else None

            gear_set.name = request.data['name']
            gear_set.bcd = bcd
            gear_set.regulator = regulator
            gear_set.octopus = octopus
            gear_set.mask = mask
            gear_set.fins = fins
            gear_set.boots = boots
            gear_set.computer = computer
            gear_set.exposure_suit = exposure_suit
            gear_set.weights = weights
            gear_set.tank = tank
            gear_set.save()

            serializer = GearSetSerializer(
                gear_set, many=False, context={"request": request})
            return Response({"message": "Gear set updated!", "gear_set": serializer.data},
                            status=status.HTTP_204_NO_CONTENT)

        except Exception as ex:
            return Response({'error': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def destroy(self, request, pk=None):
        try:
            gear_set = Gear_Set.objects.get(pk=pk, diver__user=request.auth.user)
            gear_set.delete()

            return Response({"Gear_Set deleted"}, status=status.HTTP_204_NO_CONTENT)

        except Gear_Set.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
