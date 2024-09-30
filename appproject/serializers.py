from rest_framework import serializers
from .models import Field, FieldLink

class UniqueSequenceListSerializer(serializers.ListSerializer):
    def validate(self, data):
        """
        Validate that sequences are unique within the same field.
        """
        sequences = [item['sequence'] for item in data]
        if len(sequences) != len(set(sequences)):
            raise serializers.ValidationError(
                "Sequences must be unique within the same field."
            )
        return data

class FieldChildrenSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldLink
        fields = [
            'id', 'field', 'subfield', 'sequence', 'text_before', 'text_after'
        ]
        list_serializer_class = UniqueSequenceListSerializer

    def validate_subfield(self, value):
        """
        Validate if the subfield exists.
        """
        if not Field.objects.filter(pk=value.pk).exists():
            raise serializers.ValidationError(
                f"invalid pk: {value.pk}."
            )
        return value
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        del data['field']
        return data


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = '__all__'

    def create(self, validated_data):
        obj = Field.objects.create(**validated_data)
        children_data = self.initial_data.pop('children', None)
        if children_data:
            if not isinstance(children_data, list):
                raise serializers.ValidationError(
                    "Children must be a list of objects."
                )
            for child in children_data:
                child['field'] = obj.pk
            serializer = FieldChildrenSerializer(
                data=children_data, many=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return obj

    def get_children(self, obj):
        children = FieldLink.objects.filter(field=obj)
        return FieldChildrenSerializer(children, many=True).data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['children'] = self.get_children(instance)
        return data
