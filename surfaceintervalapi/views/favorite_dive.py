from django.http import HttpResponseServerError

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from surfaceintervalapi.models import Dive, Diver, FavoriteDive, GearSet
from surfaceintervalapi.serializers import DiveSerializer


class DiveView(ModelViewSet):
    queryset = Dive.objects.all()
    serializer_class = DiveSerializer

    def retrieve(self, request, pk=None):
        try:
            dive = Dive.objects.get(pk=pk, diver__user=request.user)
            serializer = DiveSerializer(dive, context={"request": request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        dives = Dive.objects.filter(diver__user=request.user).order_by("dive_number")
        serializer = DiveSerializer(dives, many=True, context={"request": request})
        return Response(serializer.data)

    def create(self, request):
        diver = Diver.objects.get(user=request.user)
        gear_set = GearSet.objects.get(diver=diver, pk=request.data["gearSet"])
        startPressure = request.data["startPressure"]
        endPressure = request.data["endPressure"]
        startPressure = None if startPressure == 0 or endPressure > startPressure else startPressure
        endPressure = None if endPressure == 0 or endPressure > endPressure else endPressure

        try:
            dive = Dive.objects.create(
                diver=diver,
                date=request.data["date"],
                gear_set=gear_set,
                location=request.data["location"],
                site=request.data["site"],
                water=request.data["water"],
                depth=request.data["depth"],
                time=request.data["time"],
                description=request.data["description"],
                start_pressure=request.data["startPressure"],
                end_pressure=request.data["endPressure"],
                tank_vol=request.data["tankVol"],
            )

            serializer = DiveSerializer(dive, many=False, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as ex:
            return Response({"error": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, pk):
        diver = Diver.objects.get(user=request.user)
        gear_set = GearSet.objects.get(diver=diver, pk=request.data["gearSet"])

        try:
            dive = Dive.objects.get(diver=diver, pk=pk)
            dive.date = request.data["date"]
            dive.gear_set = gear_set
            dive.location = request.data["location"]
            dive.site = request.data["site"]
            dive.water = request.data["water"]
            dive.depth = request.data["depth"]
            dive.time = request.data["time"]
            dive.description = request.data["description"]
            dive.start_pressure = request.data["startPressure"]
            dive.end_pressure = request.data["endPressure"]
            dive.tank_vol = request.data["tankVol"]
            dive.save()

            serializer = DiveSerializer(dive, many=False, context={"request": request})
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

        except Exception as ex:
            return Response({"error": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        diver = Diver.objects.get(user=request.user)

        try:
            dive = Dive.objects.get(pk=pk, diver=diver)
            dive.delete()

            return Response({"Dive deleted"}, status=status.HTTP_204_NO_CONTENT)

        except Dive.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=["post", "delete"], detail=True, url_path="star")
    def star(self, request, pk):
        diver = Diver.objects.get(user=request.user)
        dive = Dive.objects.get(pk=pk, diver=diver)

        if request.method == "POST":
            try:
                FavoriteDive.objects.create(diver=diver, dive=dive)

                return Response({f"{dive.site} dive starred!"}, status=status.HTTP_201_CREATED)

            except Exception as ex:
                return Response({"error": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
