from rest_framework.response import Response
from rest_framework.views import APIView
from surfaceintervalapi.serializers import HealthCheckSerializer


class HealthCheckView(APIView):
    serializer_class = HealthCheckSerializer

    def get(self, request):
        return Response({"status": "ok"})
