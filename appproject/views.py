from rest_framework import status, generics
from rest_framework.response import Response
from django.db import transaction, IntegrityError
from django.shortcuts import get_object_or_404
from .models import Field
from .serializers import FieldSerializer

class FieldListCreateView(generics.ListCreateAPIView):
    """
    API view to list all Fields or create a new Field with 
    optional children.
    """
    queryset = Field.objects.all()
    serializer_class = FieldSerializer

    def create(self, request, *args, **kwargs):
        """
        Create new field with optional children.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            with transaction.atomic():
                serializer.save()
        except IntegrityError as e:
            error_message = self._handle_integrity_error(e)
            return Response(
                {"error": error_message}, status=status.HTTP_400_BAD_REQUEST
            )
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def _handle_integrity_error(self, error):
        """
        Database integrity process errors and returns an 
        appropriate message.
        """
        error_message = str(error).lower()
        if 'unique constraint' in error_message:
            return "Duplicated relationship."
        return "Database integrity error."
    
    def get(self, request, *args, **kwargs):
        """
        Retrieve a list Fields or get a specific Field.
        """
        field_id = kwargs.get('pk')
        if field_id:
            field = get_object_or_404(Field, pk=field_id)
            serializer = self.get_serializer(field)
            return Response(serializer.data)
        return super().get(request, *args, **kwargs)

class FieldRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete a specific Field 
    by its primary key.
    """
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        """
        Retrieve a specific Field by its pk.
        """
        field_id = kwargs.get('pk')
        field = get_object_or_404(Field, pk=field_id)
        serializer = self.get_serializer(field)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        """
        Update a specific Field by its pk.
        """
        #partial = kwargs.pop('partial', False)
        partial = False
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                serializer.save()
        except IntegrityError as e:
            error_message = self._handle_integrity_error(e)
            return Response(
                {"error": error_message}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """
        Delete a specific Field by its pk.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _handle_integrity_error(self, error):
        """
        Database integrity process errors and returns an 
        appropriate message.
        """
        error_message = str(error).lower()
        if 'unique constraint' in error_message:
            return "Duplicated relationship."
        return "Database integrity error."