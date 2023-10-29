from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from surfaceintervalapi.models import Specialty, Diver
from surfaceintervalapi.serializers import SpecialtySerializer


class SpecialtyView(ViewSet):
    def list(self, request):
        specialties = Specialty.objects.all()
        serializer = SpecialtySerializer(specialties, many=True, context={"request": request})
        return Response(serializer.data)

    def create(self, request):
        try:
            Diver.objects.get(user=request.auth.user, user__is_superuser=True)
        except Diver.DoesNotExist:
            return Response({"error": "You are not authorized."}, status=status.HTTP_403_FORBIDDEN)

        try:
            specialty = Specialty.objects.create(
                name=request.data["name"],
            )

            serializer = SpecialtySerializer(specialty, many=False, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as ex:
            return Response({"error": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            Diver.objects.get(user=request.auth.user, user__is_superuser=True)
        except Diver.DoesNotExist:
            return Response({"error": "You are not authorized."}, status=status.HTTP_403_FORBIDDEN)

        try:
            specialty = Specialty.objects.get(pk=pk)
            specialty.delete()

            return Response({"Specialty deleted"}, status=status.HTTP_204_NO_CONTENT)

        except Specialty.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
