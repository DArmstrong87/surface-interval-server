from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from surfaceintervalapi.models import Diver, CustomSpecialty
from surfaceintervalapi.serializers import CustomSpecialtySerializer


class CustomSpecialtyView(ViewSet):
    def retrieve(self, request, pk):
        custom_specialty = CustomSpecialty.objects.get(pk=pk, diver__user=request.auth.user)
        serializer = CustomSpecialtySerializer(
            custom_specialty, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def list(self, request):
        custom_specialty = CustomSpecialty.objects.filter(diver__user=request.auth.user)
        serializer = CustomSpecialtySerializer(
            custom_specialty, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def create(self, request):
        diver = Diver.objects.get(user=request.auth.user)

        try:
            custom_specialty = CustomSpecialty.objects.create(
                diver=diver,
                name=request.data["name"],
            )

            serializer = CustomSpecialtySerializer(
                custom_specialty, many=False, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as ex:
            return Response({"error": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        diver = Diver.objects.get(user=request.auth.user)

        try:
            custom_specialty = CustomSpecialty.objects.get(pk=pk, diver=diver)
            custom_specialty.delete()

            return Response({"CustomSpecialty deleted"}, status=status.HTTP_204_NO_CONTENT)

        except CustomSpecialty.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk):
        diver = Diver.objects.get(user=request.auth.user)

        try:
            custom_specialty = CustomSpecialty.objects.get(diver=diver, pk=pk)
            custom_specialty.name = request.data["name"]

            custom_specialty.save()

            serializer = CustomSpecialtySerializer(
                custom_specialty, many=False, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

        except Exception as ex:
            return Response({"error": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
