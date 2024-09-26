# tests.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Field

class FieldAPITestCase(APITestCase):
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

    def test_create_field_with_children(self):
        # Cria subfields necessários
        subfield1 = Field.objects.create(name="Subfield 1")
        subfield2 = Field.objects.create(name="Subfield 2")

        # Atualiza os dados com os pks reais
        self.field_data['children'][0]['subfield'] = subfield1.pk
        self.field_data['children'][1]['subfield'] = subfield2.pk

        response = self.client.post(self.field_url, self.field_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Field.objects.count(), 3)  # 1 principal + 2 subfields

    def test_create_field_with_invalid_subfield(self):
        self.field_data['children'][0]['subfield'] = 999  # PK inexistente

        response = self.client.post(self.field_url, self.field_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('subfield', response.data['children'][0])

    def test_list_fields(self):
        Field.objects.create(name="Campo 1")
        Field.objects.create(name="Campo 2")

        response = self.client.get(self.field_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
