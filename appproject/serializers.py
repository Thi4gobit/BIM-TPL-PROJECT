from rest_framework import serializers
from .models import *


class GroupFieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ['id', 'name']


class FieldDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='subfield.id')
    name = serializers.CharField(source='subfield.name')

    class Meta:
        model = FieldLink
        fields = ['id', 'name', 'sequence', 'text_before', 'text_after']


class FieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = Field
        fields = ['id', 'name']

    def to_representation(self, instance):
        data = super().to_representation(instance)     
        children = FieldDetailSerializer(
            FieldLink.objects.filter(field=instance.pk).all(), many=True
        ).data
        data['children'] = children
        return data






class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ['id', 'item']


class FieldRelationshipSerializer(serializers.ModelSerializer):

    class Meta:
        model = FieldLink
        fields = [
            'id', 'field', 'subfield', 'sequence', 
            'text_before', 'text_after'
        ]
        extra_kwargs = {
            'id': {'read_only': False}
        }
    
    def validate(self, data):
        field = data.get('field')
        subfield = data.get('subfield')
        if field == subfield:
            raise serializers.ValidationError(
                f"Self-relationship is forbbiden ({field})."
            )
        return data


class CustomFieldSerializer(serializers.ModelSerializer):

    field = FieldSerializer()
    group = GroupFieldSerializer()

    class Meta:
        model = FieldSet
        fields = [
            'id', 'field', 'group', 'priority', 'is_description'
        ]


class CustomServiceSerializer(serializers.ModelSerializer):

    item = ItemSerializer()
    field = CustomFieldSerializer()

    class Meta:
        model = Obj
        fields = ['id', 'item', 'field', 'value']



class CustomService2Serializer(serializers.ModelSerializer):

    field = serializers.SerializerMethodField()

    class Meta:
        model = Obj
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