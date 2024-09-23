from rest_framework import serializers
from .models import *


class GroupFieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupField
        fields = ['id', 'name']


class FieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = Field
        fields = ['id', 'name']


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ['id', 'item']


class FieldSelfRelationshipSerializer(serializers.ModelSerializer):

    # field = FieldSerializer()
    # subfield = FieldSerializer()

    class Meta:
        model = FieldSelfRelationship
        fields = [
            'id', 'field', 'subfield', 'sequence', 
            'text_before', 'text_after'
        ]
    
    def validate(self, data):
        field = data.get('field')
        subfield = data.get('subfield')
        if field == subfield:
                raise serializers.ValidationError(
                    f"Self-relationship is forbbiden ({field})."
                )
        if isinstance(self.initial_data, list):
            list_input = self.initial_data
            for i in list_input:
                if i['field'] == field and i['subfield'] == subfield:
                    raise serializers.ValidationError(
                        f"Duplicated: '{field}' and '{subfield}'."
                    )
        return data


class CustomFieldSerializer(serializers.ModelSerializer):

    field = FieldSerializer()
    group = GroupFieldSerializer()

    class Meta:
        model = CustomField
        fields = [
            'id', 'field', 'group', 'is_required', 'is_unique', 
            'priority', 'is_description', 'before_text', 'after_text'
        ]


class CustomServiceSerializer(serializers.ModelSerializer):

    item = ItemSerializer()
    field = CustomFieldSerializer()

    class Meta:
        model = CustomService
        fields = ['id', 'item', 'field', 'value']



class CustomService2Serializer(serializers.ModelSerializer):

    field = serializers.SerializerMethodField()

    class Meta:
        model = CustomService
        fields = ['field', 'value']

    def get_field(self, obj):
        return obj.field.field.name


class ItemWithCustomFieldsSerializer(serializers.ModelSerializer):

    fields = CustomService2Serializer(
        source='customfieldvalue_item', many=True
    )

    class Meta:
        model = Item
        fields = ['id', 'item', 'fields']