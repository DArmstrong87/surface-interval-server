from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from surfaceintervalapi.models import Image
from surfaceintervalapi.serializers import ImageSerializer


class ImageView(ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def list(self, request):
        images = Image.objects.filter(diver__user=request.auth.user)
        serializer = ImageSerializer(images, many=True, context={"request": request})
        return Response(serializer.data)

    def destroy(self, request, pk):
        try:
            image = Image.objects.get(pk=pk, diver__user=request.auth.user)
            image.delete()
            return Response({"Image deleted"}, status=status.HTTP_204_NO_CONTENT)

        except Image.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
