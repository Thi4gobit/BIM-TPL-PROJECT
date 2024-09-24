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


# def update_many(self, serializer):
#         if serializer.is_valid():
#             try:
#                 with transaction.atomic():
#                     data_dict = {item['id']: item for item in serializer.validated_data}
                    
#                     # Update each object
#                     for obj in FieldSelfRelationship.objects.filter(id__in=data_dict.keys()):
#                         data = data_dict[obj.id]
#                         for attr, value in data.items():
#                             setattr(obj, attr, value)
#                         obj.save()
                    
#                     return Response(serializer.data, status=status.HTTP_200_OK)
            
#             except IntegrityError as e:
#                 if 'unique constraint' in str(e).lower():
#                     return Response(
#                         {"error": "Duplicated relationship."},
#                         status=status.HTTP_400_BAD_REQUEST
#                     )
#                 else:
#                     return Response(
#                         {"error": "Database integrity error."},
#                         status=status.HTTP_400_BAD_REQUEST
#                     )
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def update_many(serializer):
    if serializer.is_valid():
        try:
            with transaction.atomic():
                # Crie um dicionário com os dados validados, filtrando apenas itens com o campo 'id'
                for item in serializer.validated_data:
                    print(item)
                data_dict = {item['id']: item for item in serializer.validated_data if 'id' in item}
                
                # Verifique o conteúdo de data_dict
                print("Data to update:", data_dict)
                
                # Obtenha os objetos que correspondem aos IDs em data_dict
                objects = FieldSelfRelationship.objects.filter(id__in=data_dict.keys())
                
                # Verifique se os objetos foram encontrados
                print("Objects found:", list(objects))
                
                updated_ids = []
                for obj in objects:
                    data = data_dict[obj.id]
                    # Atualize os atributos, exceto 'id'
                    for attr, value in data.items():
                        if attr != 'id':  # Não atualize o campo 'id'
                            setattr(obj, attr, value)
                    obj.save()
                    updated_ids.append(obj.id)
                
                # Verifique quais IDs foram atualizados
                print("Updated IDs:", updated_ids)
                
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


class FieldRelationshipListView(generics.ListAPIView):
    queryset = FieldSelfRelationship.objects.all()
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
    
    # def update_many(self, serializer):
    #     if serializer.is_valid():
    #         try:
    #             with transaction.atomic():
    #                 data_dict = {item['id']: item for item in serializer.validated_data}
                    
    #                 # Update each object
    #                 for obj in FieldSelfRelationship.objects.filter(id__in=data_dict.keys()):
    #                     data = data_dict[obj.id]
    #                     for attr, value in data.items():
    #                         setattr(obj, attr, value)
    #                     obj.save()
                    
    #                 return Response(serializer.data, status=status.HTTP_200_OK)
            
    #         except IntegrityError as e:
    #             if 'unique constraint' in str(e).lower():
    #                 return Response(
    #                     {"error": "Duplicated relationship."},
    #                     status=status.HTTP_400_BAD_REQUEST
    #                 )
    #             else:
    #                 return Response(
    #                     {"error": "Database integrity error."},
    #                     status=status.HTTP_400_BAD_REQUEST
    #                 )
        
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







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