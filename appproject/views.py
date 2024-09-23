from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import *


class GroupFieldListCreateView(generics.ListCreateAPIView):
    queryset = GroupField.objects.all()
    serializer_class = GroupFieldSerializer


class GroupFieldDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GroupField.objects.all()
    serializer_class = GroupFieldSerializer


class FieldListCreateView(generics.ListCreateAPIView):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer


class FieldDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer


class FieldSelfRelationshipCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FieldSelfRelationshipSerializer(
            data=request.data, many=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








class CustomFieldCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomFieldSerializer(data=request.data, many=True)
        if serializer.is_valid():


            if not any(item.get('is_description', False) for item in request.data):
                return Response(
                    {"error": "A field must have is_description true."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer.save()


            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class ItemListCreateView(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemWithCustomFieldsSerializer


class ItemDetailView(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemWithCustomFieldsSerializer