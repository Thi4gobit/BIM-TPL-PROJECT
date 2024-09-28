from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import *
from django.db import IntegrityError, transaction


def seek_pk(pk, model):
    try:
        return model.objects.get(pk=pk)
    except model.DoesNotExist:
        return None
    
def serializer_obj(obj, serial, data=None):
    if data:
        return serial(obj, data=data)
    return serial(obj)

def get_one(pk, model, serial, data):
    obj = seek_pk(pk, model)
    if obj:
        s = serializer_obj(obj, serial, data)
        return Response(s.data, status=status.HTTP_200_OK)
    return Response(
        {'error': 'Not found.'}, status=status.HTTP_404_NOT_FOUND
    )

def get_many(model, serial, **filters):
    objs = model.objects.filter(**filters)
    s = serial(objs, many=True)
    return Response(s.data, status=status.HTTP_200_OK)

def check_unique(serializer):
    try:
        return serializer.save()
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

def save_obj(s):
    # s = serial(data=data)
    if s.is_valid():
        obj = s.save()
    else:
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)
    return obj, s


def has_field_is_list(data, field):
    if field in data and data.get(field) and \
        isinstance(data.get(field), list):
        return True
    return False


def insert_parent_on_data(data, p_field, p_pk):
    # p - parent & c - children
    for i in data:
        i[p_field] = p_pk
    return data


def is_children_existing(data, field, c_field, c_model):
    if has_field_is_list(data, field):
        for i in data.get(field):
            if not seek_pk(i[c_field], c_model):
                return False, i[c_field]
    return True, data





def save_subojts(data, field, p_field, p_pk, serial, c_field, c_model):
    if has_field_is_list(data, field):
        data = insert_parent_on_data(
            data.get(field), p_field, p_pk, c_field, c_model
        )
        if data:
            s = serial(data=data, many=True)
            if s.is_valid():
                if check_unique(s):
                    return s
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)



# def save_subojts(data, field, p_field, p_pk, serial):
#     if field in data and data.get(field) and \
#         isinstance(data.get(field), list):
#         for i in data.get(field):
#             i[p_field] = p_pk
#         s = serial(data=data.get(field), many=True)
#         if s.is_valid():
#             if check_unique(s):
#                 return s
#         return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

def change_one(pk, model):
    try:
        obj = model.objects.get(pk=pk)
    except model.DoesNotExist:
        return Response(
            {'error': 'Not found.'}, status=status.HTTP_404_NOT_FOUND
        )

# FIELD

class FieldListOrCreateView(APIView):
    def get(self, request, *args, **kwargs):
        field_id = kwargs.get('pk')
        if field_id:
            get_one(field_id, Field, FieldSerializer)
        get_many(Field, FieldSerializer)
    
    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        model = Field
        subitem = 'children'
        p_field = 'field'
        c_field = 'subfield'
        c_model = Field
        serial1 = FieldSerializer
        serial2 = FieldChildrenSerializer
        has_children = False
        if subitem in data and data.get(subitem) and \
            isinstance(data.get(subitem), list):
            has_children = True
            for i in data.get(subitem):
                try:
                    c_model.objects.get(pk=i[c_field])
                except model.DoesNotExist:
                    return Response(
                        f"Inexisting pk: {i[c_field]}", 
                        status=status.HTTP_400_BAD_REQUEST
                    )
        with transaction.atomic():
            s1 = serial1(data=data)
            if not s1.is_valid():
                return Response(s1.errors, status=status.HTTP_400_BAD_REQUEST)
            obj = s1.save()
            if has_children:
                data = request.data.copy().get(subitem)
                for i in data:
                    i[p_field] = obj.pk
                s2 = serial2(data=data, many=True)
                if not s2.is_valid():
                    return Response(s2.errors, status=status.HTTP_400_BAD_REQUEST)
                try:
                    s2.save()
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
                return Response([s1.data, s2.data], status=status.HTTP_201_CREATED)
            return Response(s1.data, status=status.HTTP_201_CREATED)


class FieldRetrieveUpdateDeleteView(APIView):
    def get(self, request, *args, **kwargs):
        field_id = kwargs.get('pk')
        if field_id:
            get_one(field_id, Field, FieldSerializer)

    def put(self, request, *args, **kwargs):
        field_id = kwargs.get('pk')
        if field_id:
            obj = seek_pk(field_id, Field)
            if not obj:
                return Response(
                    {'error': 'Not found.'},
                    status=status.HTTP_404_NOT_FOUND
                )
            # try:
            #     field = Field.objects.get(pk=field_id)
            # except Field.DoesNotExist:
            #     return Response(
            #         {'error': 'Not found.'},
            #         status=status.HTTP_404_NOT_FOUND
            #     )
            with transaction.atomic():
                s1 = serializer_obj(obj, FieldSerializer, data=request.data)
                if s1.is_valid():
                    obj = s1.save()
                else:
                    return Response(
                        s1.errors, status=status.HTTP_400_BAD_REQUEST
                    )
                s2 = save_subojts(
                    data=request.data, field='children', p_field='field', 
                    p_pk=obj.pk, serial=FieldChildrenSerializer
                )
                if s2:
                    return Response(
                        [s1.data, s2.data], status=status.HTTP_201_CREATED
                    )
                return Response(s1.data, status=status.HTTP_201_CREATED)

                
                #serializer1 = FieldSerializer(field, data=request.data)
                # if serializer1.is_valid():
                #     obj = serializer1.save()
                # else:
                #     return Response(
                #         serializer1.errors, 
                #         status=status.HTTP_400_BAD_REQUEST
                #     )
                
        #         if 'children' in request.data and \
        #            isinstance(request.data.get('children'), list):
        #             children = request.data.get('children')
        #             for i in children:
        #                 i['field'] = obj.pk
        #             serializer2 = FieldChildrenSerializer(
        #                 data=request.data.get('children'), many=True
        #             )
        #             if serializer2.is_valid():
        #                 if check_unique(serializer2):
        #                     return Response(
        #                         [serializer1.data, serializer2.data], 
        #                         status=status.HTTP_200_OK
        #                     )
        #             return Response(
        #                 serializer2.errors, 
        #                 status=status.HTTP_400_BAD_REQUEST
        #             )
        #         return Response(
        #             serializer1.data, status=status.HTTP_200_OK
        #         )
        # return Response(
        #     {'error': 'ID not provided.'},
        #     status=status.HTTP_400_BAD_REQUEST
        # )

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
