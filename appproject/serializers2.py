# serializers.py
from rest_framework import serializers
from .models import Field

class FieldChildrenSerializer(serializers.ModelSerializer):
    subfield = serializers.PrimaryKeyRelatedField(
        queryset=Field.objects.all()
    )

    class Meta:
        model = Field
        fields = [
            'id', 'field', 'subfield', 'sequence', 'text_before', 'text_after'
        ]

    def validate_subfield(self, value):
        """
        Validate if the field exists.
        """
        if not Field.objects.filter(pk=value.pk).exists():
            raise serializers.ValidationError(
                f"Inexisting pk (subfield): {value.pk}."
            )
        return value

class FieldSerializer(serializers.ModelSerializer):
    children = FieldChildrenSerializer(many=True, required=False)

    class Meta:
        model = Field
        fields = ['id', 'name', 'template', 'children']

    def create(self, validated_data):
        children_data = validated_data.pop('children', [])
        field = Field.objects.create(**validated_data)
        
        for child_data in children_data:
            child_data['field'] = field
            FieldChildrenSerializer.create(
                FieldChildrenSerializer(), validated_data=child_data
            )
        
        return field

    def validate_children(self, value):
        """
        Validate if 'children' is a list of valid objects.
        """
        if not isinstance(value, list):
            raise serializers.ValidationError(
                "Children must be a list of objects."
            )
        return value
