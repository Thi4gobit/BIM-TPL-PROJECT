from django.test import TestCase
from django.urls import reverse
from ..models import *


URL_NEW = 'list-create-field'

class NewServicesTestCase(TestCase):

    def test_view_field_relationship_new_001(self):
        """
        children (list)
        """
        field1 = Field.objects.create(name='field1')
        field2 = Field.objects.create(name='field2')
        data = {
            'name': 'field3',
            'children': [
                {
                    'subfield': field1.pk, 
                    'sequence': 1
                }, 
                {
                    'subfield': field2.pk, 
                    'sequence': 2
                }
            ]
        }
        request = self.client.post(
            reverse(URL_NEW), data, content_type='application/json'
        )
        self.assertEqual(request.status_code, 201)
        self.assertEqual(Field.objects.all().count(), 3)
        self.assertEqual(FieldLink.objects.all().count(), 2)
        FieldLink.objects.all().delete()
        Field.objects.all().delete()


    def test_view_field_relationship_new_002(self):
        """
        children (empty list)
        """
        data = {
            'name': 'field1',
            'children': []
        }
        request = self.client.post(
            reverse(URL_NEW), data, content_type='application/json'
        )
        self.assertEqual(request.status_code, 201)
        self.assertEqual(Field.objects.all().count(), 1)
        self.assertEqual(FieldLink.objects.all().count(), 0)
        FieldLink.objects.all().delete()
        Field.objects.all().delete()


    def test_view_field_relationship_new_003(self):
        """
        children (none)
        """
        data = {
            'name': 'field1',
            'children': ''
        }
        request = self.client.post(
            reverse(URL_NEW), data, content_type='application/json'
        )
        self.assertEqual(request.status_code, 201)
        self.assertEqual(Field.objects.all().count(), 1)
        self.assertEqual(FieldLink.objects.all().count(), 0)
        FieldLink.objects.all().delete()
        Field.objects.all().delete()


    def test_view_field_relationship_new_004(self):
        """
        without children
        """
        data = {
            'name': 'field1'
        }
        request = self.client.post(
            reverse(URL_NEW), data, content_type='application/json'
        )
        self.assertEqual(request.status_code, 201)
        self.assertEqual(Field.objects.all().count(), 1)
        self.assertEqual(FieldLink.objects.all().count(), 0)
        FieldLink.objects.all().delete()
        Field.objects.all().delete()
