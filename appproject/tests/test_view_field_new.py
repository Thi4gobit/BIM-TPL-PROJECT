from django.test import TestCase
from django.urls import reverse
from ..models import *


URL_NEW = 'list-create-field'

class NewServicesTestCase(TestCase):

    def setUp(self):
        self.field_url = reverse('field-list-create')
        self.field_detail_url = lambda pk: reverse('field-detail', kwargs={'pk': pk})
        self.field_data = {
            "name": "Campo Principal",
            "children": [
                {"subfield": 1, "other_field1": "Valor1", "other_field2": "Valor2"},
                {"subfield": 2, "other_field1": "Valor3", "other_field2": "Valor4"},
            ]
        }
        
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


    def test_view_field_relationship_new_005(self):
        """
        same children (list)
        """
        field1 = Field.objects.create(name='field1')
        field2 = Field.objects.create(name='field2')
        data = {
            'name': 'field3',
            'children': [
                {
                    'subfield': field2.pk, 
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
        self.assertEqual(request.status_code, 400)
        self.assertEqual(Field.objects.all().count(), 2)
        self.assertEqual(FieldLink.objects.all().count(), 0)
        FieldLink.objects.all().delete()
        Field.objects.all().delete()