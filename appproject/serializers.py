# serializers.py
from rest_framework import serializers
from .models import Field, FieldLink

class FieldChildrenSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldLink
        fields = [
            'id', 'field', 'subfield', 'sequence', 'text_before', 'text_after'
        ]

    def validate_subfield(self, value):
        """
        Validate if the subfield exists.
        """
        if not Field.objects.filter(pk=value.pk).exists():
            raise serializers.ValidationError(
                f"invalid pk: {value.pk}."
            )
        return value

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

    # def validate_children(self, value):
    #     """
    #     Validate if 'children' is a list of valid objects.
    #     """
    #     if not isinstance(value, list):
    #         raise serializers.ValidationError(
    #             "Children must be a list of objects."
    #         )
    #     return value

    # def get_children(self, obj):
    #     children = FieldLink.objects.filter(field=obj)
    #     return FieldChildrenSerializer(children, many=True).data

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     data['children'] = self.get_children(instance)
    #     return data
    
    # def to_representation(self, instance):
    #     data = super().to_representation(instance)     
    #     children = FieldChildrenSerializer(
    #         FieldLink.objects.filter(field=instance.pk).all(), 
    #         many=True
    #     ).data
    #     data['children'] = children
    #     return data

    # def get_children(self, obj):
    #     children = FieldLink.objects.filter(field=obj)
    #     return FieldChildrenSerializer(children, many=True).data