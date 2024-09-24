from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import *
from django.db import IntegrityError, transaction


def check_unique(serializer):
    if serializer.is_valid():
        try:
            with transaction.atomic():
                serializer.save()
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
        except IntegrityError as e:
            if 'unique constraint' in str(e).lower():
                return Response(
                    {"error": "Duplicated relationship."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                return Response(
                    {"error": "Database integrity error."},
                    status=status.HTTP_400_BAD_REQUEST
                )
    return Response(
        serializer.errors, status=status.HTTP_400_BAD_REQUEST
    )


def update_many(serializer):
    if serializer.is_valid():
        try:
            with transaction.atomic():
                for item in serializer.validated_data:
                    print(item)
                data_dict = {item['id']: item for item in serializer.validated_data if 'id' in item}
                objects = FieldLink.objects.filter(id__in=data_dict.keys())
                updated_ids = []
                for obj in objects:
                    data = data_dict[obj.id]
                    for attr, value in data.items():
                        if attr != 'id':
                            setattr(obj, attr, value)
                    obj.save()
                    updated_ids.append(obj.id)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except IntegrityError as e:
            if 'unique constraint' in str(e).lower():
                return Response(
                    {"error": "Duplicated relationship."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                return Response(
                    {"error": "Database integrity error."},
                    status=status.HTTP_400_BAD_REQUEST
                )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#-----------------------------------------------------------------------
class GroupFieldListCreateView(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupFieldSerializer


class GroupFieldDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupFieldSerializer
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------

# FIELD
class FieldListCreateView(generics.ListCreateAPIView):
    serializer_class = FieldSerializer

    def get_queryset(self):
        return Field.objects.prefetch_related('fieldlink_fields').all()


class FieldDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
    
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
class FieldRelationshipListView(generics.ListAPIView):
    queryset = FieldLink.objects.all()
    serializer_class = FieldRelationshipSerializer


class FieldRelationshipCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FieldRelationshipSerializer(
            data=request.data, many=True
        )
        return check_unique(serializer)


class FieldRelationshipUpdateListView(APIView):
    def put(self, request, *args, **kwargs):
        serializer = FieldRelationshipSerializer(
            data=request.data, many=True
        )
        return update_many(serializer)
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------






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