from django.db import IntegrityError
from django.http import HttpResponseServerError

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from surfaceintervalapi.models import Dive, Diver, FavoriteDive, GearSet, Image
from surfaceintervalapi.serializers import DiveSerializer, ImageSerializer


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
        dives = Dive.objects.filter(diver__user=request.user).order_by("date", "id")
        serializer = DiveSerializer(dives, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        try:
            diver = Diver.objects.get(user=request.user)
        except Diver.DoesNotExist as ex:
            return Response({"error": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        try:
            gear_set = GearSet.objects.get(diver=diver, pk=request.data["gearSet"])
        except:
            gear_set = None

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
        if diver is None:
            return Response(
                {"error": f"Diver of id {request.user.id} does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        submitted_keys = request.data.keys()

        try:
            dive = Dive.objects.get(diver=diver, pk=pk)

            for key in submitted_keys:
                if hasattr(dive, key):
                    setattr(dive, key, request.data.get(key))
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

                return Response({f"{dive.site} dive starred! 🌟"}, status=status.HTTP_201_CREATED)
            except IntegrityError as ex:
                if "UNIQUE constraint failed" in ex.args[0]:
                    return Response(
                        {"error": f"{dive.site} has already been starred."},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
            except Exception as ex:
                return Response({"error": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # DELETE
        else:
            try:
                favorite = FavoriteDive.objects.get(diver=diver, dive=dive)
                favorite.delete()
                return Response({f"{dive.site} dive unstarred."}, status=status.HTTP_204_NO_CONTENT)
            except FavoriteDive.DoesNotExist:
                return Response(
                    {"error": "Favorite dive does not exist."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

    @action(methods=["get"], detail=True, url_path="images")
    def get_dive_images(self, request, pk):
        images = Image.objects.filter(diver__user=request.user, dive=pk)
        serializer = ImageSerializer(images, many=True, context={"request": request})
        return Response(serializer.data)
