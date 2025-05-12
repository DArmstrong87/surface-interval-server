from django.http import HttpResponseServerError
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from surfaceintervalapi.models import Diver, CertificationCard
from surfaceintervalapi.serializers import CertCardSerializer


class CertCardView(ModelViewSet):
    queryset = CertificationCard.objects.all()
    serializer_class = CertCardSerializer

    def retrieve(self, request, pk=None):
        try:
            cert = CertificationCard.objects.get(pk=pk, diver__user=request.auth.user)
            serializer = CertCardSerializer(cert, context={"request": request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        cert_cards = CertificationCard.objects.filter(diver__user=request.auth.user)
        serializer = CertCardSerializer(cert_cards, many=True, context={"request": request})
        return Response(serializer.data)

    def create(self, request):
        diver = Diver.objects.get(user=request.auth.user)

        try:
            cert = CertificationCard.objects.create(
                diver=diver,
                name=request.data["name"],
                date_issued=request.data["date_issued"],
                image_front_url=request.data["image_front_url"],
                image_back_url=request.data["image_back_url"],
            )

            serializer = CertCardSerializer(cert, many=False, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as ex:
            return Response({"error": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, pk):
        diver = Diver.objects.get(user=request.auth.user)

        try:
            cert = CertificationCard.objects.get(diver=diver, pk=pk)
            cert.name = request.data["name"]
            cert.date_issued = request.data["date_issued"]
            cert.image_front_url = request.data["image_front_url"]
            cert.image_back_url = request.data["image_back_url"]
            cert.save()

            serializer = CertCardSerializer(cert, many=False, context={"request": request})
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

        except Exception as ex:
            return Response({"error": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        diver = Diver.objects.get(user=request.auth.user)

        try:
            cert = CertificationCard.objects.get(pk=pk, diver=diver)
            cert.delete()

            return Response({"Cert deleted"}, status=status.HTTP_204_NO_CONTENT)

        except CertificationCard.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
