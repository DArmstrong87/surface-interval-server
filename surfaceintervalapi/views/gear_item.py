from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from surfaceintervalapi.models import Diver, Gear_Item, Custom_Gear_Type, Gear_Type
from surfaceintervalapi.serializers import GearItemSerializer


class GearItemView(ViewSet):

    def retrieve(self, request, pk):
        gear_item = Gear_Item.objects.get(pk=pk, diver__user=request.auth.user)
        serializer = GearItemSerializer(
            gear_item, many=False, context={'request': request})
        return Response(serializer.data)
    
    
    def list(self, request):
        gear_items = Gear_Item.objects.filter(diver__user=request.auth.user)
        serializer = GearItemSerializer(
            gear_items, many=True, context={'request': request})
        return Response(serializer.data)


    def create(self, request):
        diver = Diver.objects.get(user=request.auth.user)
        try:
            gear_type = Gear_Type.objects.get(pk=request.data['gear_type'])
            custom_gear_type=None
        except:
            custom_gear_type = Custom_Gear_Type.objects.get(pk=request.data['custom_gear_type'])
            gear_type = None
        
        try:
            gear_item = Gear_Item.objects.create(
                diver=diver,
                name=request.data['name'],
                gear_type=gear_type,
                custom_gear_type=custom_gear_type,
                purchase_date=request.data['purchase_date'],
                last_serviced=request.data['last_serviced'],
            )
            
            serializer = GearItemSerializer(
                gear_item, many=False, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as ex:
            return Response({'error': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def partial_update(self, request, pk):
        try:
            diver = Diver.objects.get(user=request.auth.user),
            gear_item = Gear_Item.objects.get(pk=pk, diver=diver)
        
            gear_item.name = request.data['name'],
            gear_item.gear_type = request.data['gear_type'],
            gear_item.custom_gear_type = request.data['custom_gear_type'],
            gear_item.purchase_date = request.data['purchase_date'],
            gear_item.last_serviced = request.data['last_serviced']
            gear_item.save()
            
            serializer = GearItemSerializer(
                gear_item, many=False, context={"request": request})
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
            
        except Exception as ex:
            return Response({'error': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
    def destroy(self, request, pk=None):
        try:
            gear_item = Gear_Item.objects.get(pk=pk, diver__user=request.auth.user)
            gear_item.delete()

            return Response({"Gear_Item deleted"}, status=status.HTTP_204_NO_CONTENT)

        except Gear_Item.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)