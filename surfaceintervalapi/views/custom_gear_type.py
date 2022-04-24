from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from surfaceintervalapi.models import Diver, Custom_Gear_Type
from surfaceintervalapi.serializers import CustomGearTypeSerializer


class CustomGearTypeView(ViewSet):

    def list(self, request):
        custom_gear_type = Custom_Gear_Type.objects.filter(diver__user=request.auth.user)
        serializer = CustomGearTypeSerializer(
            custom_gear_type, many=True, context={'request': request})
        return Response(serializer.data)


    def create(self, request):
        diver = Diver.objects.get(user=request.auth.user)
        
        try:
            custom_gear_type = Custom_Gear_Type.objects.create(
                diver=diver,
                name=request.data['name'],
            )
            
            serializer = CustomGearTypeSerializer(
                custom_gear_type, many=False, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as ex:
            return Response({'error': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
    def destroy(self, request, pk=None):
        diver = Diver.objects.get(user=request.auth.user)
        
        try:
            custom_gear_type = Custom_Gear_Type.objects.get(pk=pk, diver=diver)
            custom_gear_type.delete()

            return Response({"Custom_Gear_Type deleted"}, status=status.HTTP_204_NO_CONTENT)

        except Custom_Gear_Type.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
        
    def partial_update(self, request, pk):
        diver = Diver.objects.get(user=request.auth.user)

        try:
            custom_gear_type = Custom_Gear_Type.objects.get(diver=diver, pk=pk)
            custom_gear_type.name=request.data['name']

            custom_gear_type.save()
            
            serializer = CustomGearTypeSerializer(
                custom_gear_type, many=False, context={"request": request})
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
            
        except Exception as ex:
            return Response({'error': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
