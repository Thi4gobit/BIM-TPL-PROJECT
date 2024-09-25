from rest_framework import serializers
from .models import *


class FieldChildrenSerializer(serializers.ModelSerializer):

    class Meta:
        model = FieldLink
        fields = [
            'id', 'field', 'subfield', 
            'sequence', 'text_before', 'text_after'
        ]


class FieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = Field
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)     
        children = FieldChildrenSerializer(
            FieldLink.objects.filter(field=instance.pk).all(), 
            many=True
        ).data
        data['children'] = children
        return data


class GroupSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupSet
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)     
        fields = GroupSetSerializer(
            GroupSet.objects.filter(group=instance.pk).all(), 
            many=True
        ).data
        data['fields'] = fields
        return data

