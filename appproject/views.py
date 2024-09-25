from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import *
from django.db import IntegrityError, transaction


def get_one(pk, model, serial):
    try:
        obj = model.objects.get(pk=pk)
        s = serial(obj)
        return Response(s.data, status=status.HTTP_200_OK)
    except model.DoesNotExist:
        return Response(
            {'error': 'Not found.'}, status=status.HTTP_404_NOT_FOUND
        )

def get_many(model, serial):
    objs = model.objects.all()
    s = serial(objs, many=True)
    return Response(s.data, status=status.HTTP_200_OK)

def saved_serialized_obj(data, serial):
    s = serial(data=data)
    if s.is_valid():
        obj = s.save()
    else:
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)
    return obj, s

def check_unique(serializer):
    try:
        obj = serializer.save()
        return obj
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

def save_dependent_objs(data, field, p_field, p_pk, serial):
    if field in data and data.get(field) and \
        isinstance(data.get(field), list):
        for i in data.get(field):
            i[p_field] = p_pk
        s = serial(data=data.get(field), many=True)
        if s.is_valid():
            if check_unique(s):
                return s
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)




# FIELD

class FieldListOrCreateView(APIView):
    def get(self, request, *args, **kwargs):
        field_id = kwargs.get('pk')
        if field_id:
            get_one(field_id, Field, FieldSerializer)
        get_many(Field, FieldSerializer)
    
    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            obj, s1 = saved_serialized_obj(request.data, FieldSerializer)
            s2 = save_dependent_objs(
                data=request.data, field='children', p_field='field', 
                p_pk=obj.pk, serial=FieldChildrenSerializer
            )
            if s2:
                return Response(
                    [s1.data, s2.data], status=status.HTTP_201_CREATED
                )
            return Response(s1.data, status=status.HTTP_201_CREATED)


class FieldRetrieveUpdateDeleteView(APIView):
    def get(self, request, *args, **kwargs):
        field_id = kwargs.get('pk')
        if field_id:
            try:
                field = Field.objects.get(pk=field_id)
                serializer = FieldSerializer(field)
                return Response(
                    serializer.data, 
                    status=status.HTTP_200_OK
                )
            except Field.DoesNotExist:
                return Response(
                    {'error': 'Not found.'},
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response(
            {'error': 'ID not provided.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    def put(self, request, *args, **kwargs):
        field_id = kwargs.get('pk')
        if field_id:
            try:
                field = Field.objects.get(pk=field_id)
            except Field.DoesNotExist:
                return Response(
                    {'error': 'Not found.'},
                    status=status.HTTP_404_NOT_FOUND
                )
            with transaction.atomic():
                serializer1 = FieldSerializer(field, data=request.data)
                if serializer1.is_valid():
                    obj = serializer1.save()
                else:
                    return Response(
                        serializer1.errors, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                if 'children' in request.data and \
                   isinstance(request.data.get('children'), list):
                    children = request.data.get('children')
                    for i in children:
                        i['field'] = obj.pk
                    serializer2 = FieldChildrenSerializer(
                        data=request.data.get('children'), many=True
                    )
                    if serializer2.is_valid():
                        if check_unique(serializer2):
                            return Response(
                                [serializer1.data, serializer2.data], 
                                status=status.HTTP_200_OK
                            )
                    return Response(
                        serializer2.errors, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                return Response(
                    serializer1.data, status=status.HTTP_200_OK
                )
        return Response(
            {'error': 'ID not provided.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, *args, **kwargs):
        field_id = kwargs.get('pk')
        if field_id:
            try:
                field = Field.objects.get(pk=field_id)
                field.delete()
                return Response(
                    {'message': 'Deleted successfully.'},
                    status=status.HTTP_204_NO_CONTENT
                )
            except Field.DoesNotExist:
                return Response(
                    {'error': 'Not found.'},
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response(
            {'error': 'ID not provided.'},
            status=status.HTTP_400_BAD_REQUEST
        )


# GROUP

class GroupListOrCreateView(APIView):
    def get(self, request, *args, **kwargs):
        group_id = kwargs.get('pk')
        if group_id:
            try:
                group = Group.objects.get(pk=group_id)
                serializer = GroupSerializer(group)
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
            except Group.DoesNotExist:
                return Response(
                    {'error': 'Not found.'},
                    status=status.HTTP_404_NOT_FOUND
                )
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            serializer1 = GroupSerializer(data=request.data)
            if serializer1.is_valid():
                obj = serializer1.save()
            else:
                return Response(
                    serializer1.errors, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            if 'fields' in request.data and \
                request.data.get('fields') and \
                    isinstance(request.data.get('fields'), list):
                fields = request.data.get('fields')
                for i in fields:
                    i['group'] = obj.pk
                serializer2 = GroupSetSerializer(
                    data=request.data.get('fields'), many=True
                )
                if serializer2.is_valid():
                    if check_unique(serializer2):
                        return Response(
                            [serializer1.data, serializer2.data], 
                            status=status.HTTP_201_CREATED
                        )
                return Response(
                    serializer2.errors, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(
                serializer1.data, status=status.HTTP_201_CREATED
            )


class GroupRetrieveUpdateDeleteView(APIView):
    def get(self, request, *args, **kwargs):
        group_id = kwargs.get('pk')
        if group_id:
            try:
                group = Group.objects.get(pk=group_id)
                serializer = GroupSerializer(group)
                return Response(
                    serializer.data, 
                    status=status.HTTP_200_OK
                )
            except Group.DoesNotExist:
                return Response(
                    {'error': 'Not found.'},
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response(
            {'error': 'ID not provided.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    def put(self, request, *args, **kwargs):
        group_id = kwargs.get('pk')
        if group_id:
            try:
                group = Group.objects.get(pk=group_id)
            except Group.DoesNotExist:
                return Response(
                    {'error': 'Not found.'},
                    status=status.HTTP_404_NOT_FOUND
                )
            with transaction.atomic():
                serializer1 = GroupSerializer(group, data=request.data)
                if serializer1.is_valid():
                    obj = serializer1.save()
                else:
                    return Response(
                        serializer1.errors, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                if 'children' in request.data and \
                   isinstance(request.data.get('children'), list):
                    children = request.data.get('children')
                    for i in children:
                        i['group'] = obj.pk
                    serializer2 = GroupSetSerializer(
                        data=request.data.get('children'), many=True
                    )
                    if serializer2.is_valid():
                        if check_unique(serializer2):
                            return Response(
                                [serializer1.data, serializer2.data], 
                                status=status.HTTP_200_OK
                            )
                    return Response(
                        serializer2.errors, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                return Response(
                    serializer1.data, status=status.HTTP_200_OK
                )
        return Response(
            {'error': 'ID not provided.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, *args, **kwargs):
        group_id = kwargs.get('pk')
        if group_id:
            try:
                group = Group.objects.get(pk=group_id)
                group.delete()
                return Response(
                    {'message': 'Deleted successfully.'},
                    status=status.HTTP_204_NO_CONTENT
                )
            except Group.DoesNotExist:
                return Response(
                    {'error': 'Not found.'},
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response(
            {'error': 'ID not provided.'},
            status=status.HTTP_400_BAD_REQUEST
        )








# class CustomFieldCreateView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = CustomFieldSerializer(data=request.data, many=True)
#         if serializer.is_valid():


#             if not any(item.get('is_description', False) for item in request.data):
#                 return Response(
#                     {"error": "A field must have is_description true."},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
#             serializer.save()


#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
