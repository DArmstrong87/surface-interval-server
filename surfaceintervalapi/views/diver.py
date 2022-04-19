
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from surfaceintervalapi.models import Diver
from surfaceintervalapi.serializers import DiverSerializer


class DiverView(ViewSet):

    def retrieve(self, request, pk=None):
        try:
            diver = Diver.objects.get(pk=pk, user=request.auth.user)
            serializer = DiverSerializer(diver, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
