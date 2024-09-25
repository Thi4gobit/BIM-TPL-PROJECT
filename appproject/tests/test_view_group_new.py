from django.test import TestCase
from django.urls import reverse
from ..models import *


URL_NEW = 'list-create-group'

class NewServicesTestCase(TestCase):

    def test_view_group_new_001(self):
        """
        fields (list)
        """
        field1 = Field.objects.create(name='field1')
        field2 = Field.objects.create(name='field2')
        data = {
            'name': 'group1',
            'fields': [
                {
                    'field': field1.pk, 
                }, 
                {
                    'field': field2.pk, 
                }
            ]
        }
        request = self.client.post(
            reverse(URL_NEW), data, content_type='application/json'
        )
        self.assertEqual(request.status_code, 201)
        self.assertEqual(Field.objects.all().count(), 2)
        self.assertEqual(Group.objects.all().count(), 1)
        Group.objects.all().delete()
        Field.objects.all().delete()


    def test_view_group_new_002(self):
        """
        fields (empty list)
        """
        data = {
            'name': 'group1',
            'fields': []
        }
        request = self.client.post(
            reverse(URL_NEW), data, content_type='application/json'
        )
        self.assertEqual(request.status_code, 201)
        self.assertEqual(Field.objects.all().count(), 0)
        self.assertEqual(Group.objects.all().count(), 1)
        Group.objects.all().delete()
        Field.objects.all().delete()


    def test_view_group_new_003(self):
        """
        fields (none)
        """
        data = {
            'name': 'group1',
            'fields': ''
        }
        request = self.client.post(
            reverse(URL_NEW), data, content_type='application/json'
        )
        self.assertEqual(request.status_code, 201)
        self.assertEqual(Field.objects.all().count(), 0)
        self.assertEqual(Group.objects.all().count(), 1)
        Group.objects.all().delete()
        Field.objects.all().delete()


    def test_view_group_new_004(self):
        """
        without fields
        """
        data = {
            'name': 'group1',
        }
        request = self.client.post(
            reverse(URL_NEW), data, content_type='application/json'
        )
        self.assertEqual(request.status_code, 201)
        self.assertEqual(Field.objects.all().count(), 0)
        self.assertEqual(Group.objects.all().count(), 1)
        Group.objects.all().delete()
        Field.objects.all().delete()
