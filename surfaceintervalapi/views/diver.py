from django.http import HttpResponseServerError

from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from surfaceintervalapi.models import Diver
from surfaceintervalapi.serializers import DiverSerializer


class DiverView(ViewSet):
    def list(self, request):
        try:
            diver = Diver.objects.get(user=request.auth.user)
            serializer = DiverSerializer(diver, context={"request": request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def partial_update(self, request, pk):
        try:
            diver = Diver.objects.get(user=request.auth.user)
            user = request.auth.user

            diver.units = request.data["units"]
            user.first_name = request.data["first_name"]
            user.last_name = request.data["last_name"]

            user.save()
            diver.save()

            serializer = DiverSerializer(diver, many=False, context={"request": request})
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

        except Exception as ex:
            return Response({"error": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
