# tests.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from ..models import Field, FieldLink

class FieldAPITestCase(APITestCase):
    def setUp(self):
        self.field_url = reverse('field-list-create')
        self.field_detail_url = lambda pk: reverse(
            'field-detail', kwargs={'pk': pk}
        )
        self.field_data = {
            'name': 'name',
            'children': [
                {'subfield': 1, 'sequence': 1},
                {'subfield': 2, 'sequence': 2}
            ]
        }

    def test_create_field_without_children(self):
        data = self.field_data.copy()
        del data['children']
        response = self.client.post(self.field_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Field.objects.count(), 1)
        self.assertEqual(FieldLink.objects.count(), 0)
        Field.objects.all().delete()

    def test_create_field_with_children_none(self):
        data = self.field_data.copy()
        data['children'] = None
        response = self.client.post(self.field_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Field.objects.count(), 1)
        self.assertEqual(FieldLink.objects.count(), 0)
    
    def test_create_field_with_children_not_list(self):
        data = self.field_data.copy()
        data['children'] = 'I am not a list'
        response = self.client.post(self.field_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Field.objects.count(), 0)
        self.assertEqual(FieldLink.objects.count(), 0)

    def test_create_field_with_children_empty(self):
        data = self.field_data.copy()
        data['children'] = []
        response = self.client.post(self.field_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Field.objects.count(), 1)
        self.assertEqual(FieldLink.objects.count(), 0)
        Field.objects.all().delete()

    def test_create_field_with_children(self):
        data = self.field_data.copy()
        subfield1 = Field.objects.create(name='Subfield 1')
        subfield2 = Field.objects.create(name='Subfield 2')
        data['children'][0]['subfield'] = subfield1.pk
        data['children'][1]['subfield'] = subfield2.pk
        response = self.client.post(self.field_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Field.objects.count(), 3)
        self.assertEqual(FieldLink.objects.count(), 2)
        FieldLink.objects.all().delete()
        Field.objects.all().delete()

    # def test_create_field_with_invalid_subfield(self):
    #     data = self.field_data.copy()
    #     data['children'][0]['subfield'] = 999
    #     response = self.client.post(
    #         self.field_url, self.field_data, format='json'
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(Field.objects.count(), 0)
    #     self.assertEqual(FieldLink.objects.count(), 0)

    # def test_list_fields(self):
    #     Field.objects.create(name="Campo 1")
    #     Field.objects.create(name="Campo 2")

    #     response = self.client.get(self.field_url, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data), 2)
    #     FieldLink.objects.all().delete()
    #     Field.objects.all().delete()
