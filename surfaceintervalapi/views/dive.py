from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from surfaceintervalapi.models import Dive, Diver
from surfaceintervalapi.models.gear_set import Gear_Set
from surfaceintervalapi.serializers import DiveSerializer


class DiveView(ViewSet):

    def retrieve(self, request, pk=None):
        try:
            dive = Dive.objects.get(pk=pk, diver__user=request.auth.user)
            serializer = DiveSerializer(dive, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        dives = Dive.objects.filter(diver__user=request.auth.user)
        serializer = DiveSerializer(
            dives, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        diver = Diver.objects.get(user=request.auth.user)
        gear_set = Gear_Set.objects.get(diver=diver, pk=request.data['gear_set'])
        
        try:
            dive = Dive.objects.create(
                diver=diver,
                date=request.data['date'],
                gear_set=gear_set,
                country_state=request.data['country_state'],
                site=request.data['site'],
                water=request.data['water'],
                depth=request.data['depth'],
                time=request.data['time'],
                description=request.data['description'],
                start_pressure=request.data['start_pressure'],
                end_pressure=request.data['end_pressure'],
                tank_vol=request.data['tank_vol']
            )
            
            serializer = DiveSerializer(
                dive, many=False, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as ex:
            return Response({'error': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def partial_update(self, request, pk):
        diver = Diver.objects.get(user=request.auth.user)
        gear_set = Gear_Set.objects.get(diver=diver, pk=request.data['gear_set'])

        try:
            dive = Dive.objects.get(diver=diver, pk=pk)
            dive.date=request.data['date']
            dive.gear_set=gear_set
            dive.country_state=request.data['country_state']
            dive.site=request.data['site']
            dive.water=request.data['water']
            dive.depth=request.data['depth']
            dive.time=request.data['time']
            dive.description=request.data['description']
            dive.start_pressure=request.data['start_pressure']
            dive.end_pressure=request.data['end_pressure']
            dive.tank_vol=request.data['tank_vol']
            dive.save()
            
            serializer = DiveSerializer(
                dive, many=False, context={"request": request})
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
            
        except Exception as ex:
            return Response({'error': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def destroy(self, request, pk=None):
        diver = Diver.objects.get(user=request.auth.user)
        
        try:
            dive = Dive.objects.get(pk=pk, diver=diver)
            dive.delete()

            return Response({"Dive deleted"}, status=status.HTTP_204_NO_CONTENT)

        except Dive.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)