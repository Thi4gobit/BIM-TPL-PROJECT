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

    # children
    def test_001_create_field_with_children(self):
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

    def test_002_create_field_without_children(self):
        data = self.field_data.copy()
        del data['children']
        response = self.client.post(self.field_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Field.objects.count(), 1)
        self.assertEqual(FieldLink.objects.count(), 0)
        Field.objects.all().delete()

    def test_003_create_field_with_children_none(self):
        data = self.field_data.copy()
        data['children'] = None
        response = self.client.post(self.field_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Field.objects.count(), 1)
        self.assertEqual(FieldLink.objects.count(), 0)
    
    def test_004_create_field_with_children_not_list(self):
        data = self.field_data.copy()
        data['children'] = 'I am not a list'
        response = self.client.post(self.field_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Field.objects.count(), 0)
        self.assertEqual(FieldLink.objects.count(), 0)

    def test_005_create_field_with_children_empty(self):
        data = self.field_data.copy()
        data['children'] = []
        response = self.client.post(self.field_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Field.objects.count(), 1)
        self.assertEqual(FieldLink.objects.count(), 0)
        Field.objects.all().delete()

    



    # name
    def test_006_create_field_with_duplicated_name(self):
        field1 = Field.objects.create(name='name')
        data = self.field_data.copy()
        del data['children']
        data['name'] = field1.name
        response = self.client.post(self.field_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Field.objects.count(), 1)
        self.assertEqual(FieldLink.objects.count(), 0)
        Field.objects.all().delete()

    def test_007_create_field_with_null_name(self):
        data = self.field_data.copy()
        del data['children']
        data['name'] = None
        response = self.client.post(self.field_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Field.objects.count(), 0)
        self.assertEqual(FieldLink.objects.count(), 0)

    def test_008_create_field_with_blank_name(self):
        data = self.field_data.copy()
        del data['children']
        data['name'] = ''
        response = self.client.post(self.field_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Field.objects.count(), 0)
        self.assertEqual(FieldLink.objects.count(), 0)

    def test_009_create_field_without_name(self):
        data = self.field_data.copy()
        del data['children']
        del data['name']
        response = self.client.post(self.field_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Field.objects.count(), 0)
        self.assertEqual(FieldLink.objects.count(), 0)

    def test_010_create_field_with_33_char_in_name(self):
        data = self.field_data.copy()
        del data['children']
        data['name'] = 'less than 32 char xxxxxxxxxxxxxxx'
        response = self.client.post(self.field_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Field.objects.count(), 0)
        self.assertEqual(FieldLink.objects.count(), 0)

    # children.subfield
    def test_011_create_field_with_null_subfield(self):
        data = self.field_data.copy()
        data['children'][0]['subfield'] = None
        del data['children'][1]
        response = self.client.post(self.field_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Field.objects.count(), 0)
        self.assertEqual(FieldLink.objects.count(), 0)

    def test_012_create_field_with_blank_subfield(self):
        data = self.field_data.copy()
        data['children'][0]['subfield'] = ''
        del data['children'][1]
        response = self.client.post(self.field_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Field.objects.count(), 0)
        self.assertEqual(FieldLink.objects.count(), 0)

    def test_013_create_field_with_inexisting_subfield(self):
        data = self.field_data.copy()
        data['children'][0]['subfield'] = 999
        del data['children'][1]
        response = self.client.post(self.field_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Field.objects.count(), 0)
        self.assertEqual(FieldLink.objects.count(), 0)

    def test_014_create_field_with_duplicated_subfield(self):
        data = self.field_data.copy()
        subfield1 = Field.objects.create(name='Subfield 1')
        data['children'][0]['subfield'] = subfield1.pk
        data['children'][1]['subfield'] = subfield1.pk
        response = self.client.post(self.field_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Field.objects.count(), 1)
        self.assertEqual(FieldLink.objects.count(), 0)
        Field.objects.all().delete()
    
    def test_015_create_field_with_same_subfield(self):
        data = self.field_data.copy()
        subfield1 = Field.objects.create(name='Subfield 1')
        subfield2 = Field.objects.create(name='Subfield 2')
        FieldLink.objects.create(field=subfield1, subfield=subfield2, sequence=1)
        data['children'][0]['subfield'] = subfield2.pk
        del data['children'][1]
        response = self.client.post(self.field_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Field.objects.count(), 3)
        self.assertEqual(FieldLink.objects.count(), 2)
        FieldLink.objects.all().delete()
        Field.objects.all().delete()

    # children.sequence
    def test_016_create_field_with_negative_sequence(self):
        data = self.field_data.copy()
        subfield1 = Field.objects.create(name='Subfield 1')
        data['children'][0]['subfield'] = subfield1.pk
        data['children'][0]['sequence'] = -1
        del data['children'][1]
        response = self.client.post(self.field_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Field.objects.count(), 1)
        self.assertEqual(FieldLink.objects.count(), 0)
        Field.objects.all().delete()

    def test_017_create_field_with_old_sequence(self):
        data = self.field_data.copy()
        subfield1 = Field.objects.create(name='Subfield 1')
        data['children'][0]['subfield'] = subfield1.pk
        data['children'][0]['sequence'] = 0
        del data['children'][1]
        response = self.client.post(self.field_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Field.objects.count(), 2)
        self.assertEqual(FieldLink.objects.count(), 1)
        FieldLink.objects.all().delete()
        Field.objects.all().delete()

    def test_018_create_field_with_null_sequence(self):
        data = self.field_data.copy()
        subfield1 = Field.objects.create(name='Subfield 1')
        data['children'][0]['subfield'] = subfield1.pk
        data['children'][0]['sequence'] = None
        del data['children'][1]
        response = self.client.post(self.field_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Field.objects.count(), 1)
        self.assertEqual(FieldLink.objects.count(), 0)
        Field.objects.all().delete()

    def test_019_create_field_with_blank_sequence(self):
        data = self.field_data.copy()
        subfield1 = Field.objects.create(name='Subfield 1')
        data['children'][0]['subfield'] = subfield1.pk
        data['children'][0]['sequence'] = ''
        del data['children'][1]
        response = self.client.post(self.field_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Field.objects.count(), 1)
        self.assertEqual(FieldLink.objects.count(), 0)
        Field.objects.all().delete()

    def test_020_create_field_without_sequence(self):
        data = self.field_data.copy()
        subfield1 = Field.objects.create(name='Subfield 1')
        data['children'][0]['subfield'] = subfield1.pk
        del data['children'][0]['sequence']
        del data['children'][1]
        response = self.client.post(self.field_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Field.objects.count(), 1)
        self.assertEqual(FieldLink.objects.count(), 0)
        Field.objects.all().delete()
    
    def test_021_create_field_with_sequence_not_a_integer(self):
        data = self.field_data.copy()
        subfield1 = Field.objects.create(name='Subfield 1')
        data['children'][0]['subfield'] = subfield1.pk
        data['children'][0]['sequence'] = 'I am not a integer'
        del data['children'][1]
        response = self.client.post(self.field_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Field.objects.count(), 1)
        self.assertEqual(FieldLink.objects.count(), 0)
        Field.objects.all().delete()

    def test_022_create_field_with_duplicated_sequence_to_same_field(self):
        data = self.field_data.copy()
        subfield1 = Field.objects.create(name='Subfield 1')
        subfield2 = Field.objects.create(name='Subfield 2')
        data['children'][0]['subfield'] = subfield1.pk
        data['children'][0]['sequence'] = 1
        data['children'][1]['subfield'] = subfield2.pk
        data['children'][1]['sequence'] = 1
        response = self.client.post(self.field_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Field.objects.count(), 2)
        self.assertEqual(FieldLink.objects.count(), 0)
        Field.objects.all().delete()
    
    def test_023_create_field_with_duplicated_sequence_to_same_field(self):
        data = self.field_data.copy()
        subfield1 = Field.objects.create(name='Subfield 1')
        subfield2 = Field.objects.create(name='Subfield 2')
        subfield3 = Field.objects.create(name='Subfield 3')
        FieldLink.objects.create(field=subfield1, subfield=subfield2, sequence=1)
        data['children'][0]['subfield'] = subfield2.pk
        data['children'][0]['sequence'] = 1
        del data['children'][1]
        response = self.client.post(self.field_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Field.objects.count(), 4)
        self.assertEqual(FieldLink.objects.count(), 2)
        FieldLink.objects.all().delete()
        Field.objects.all().delete()

    # children.text_before
    def test_024_create_field_with_text_before(self):
        data = self.field_data.copy()
        subfield1 = Field.objects.create(name='Subfield 1')
        data['children'][0]['subfield'] = subfield1.pk
        data['children'][0]['text_before'] = 'test_before'
        del data['children'][1]
        response = self.client.post(self.field_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Field.objects.count(), 2)
        self.assertEqual(FieldLink.objects.count(), 1)
        FieldLink.objects.all().delete()
        Field.objects.all().delete()

    def test_025_create_field_with_33_char_in_text_before(self):
        data = self.field_data.copy()
        subfield1 = Field.objects.create(name='Subfield 1')
        data['children'][0]['subfield'] = subfield1.pk
        data['children'][0]['text_before'] = 'less than 32 char xxxxxxxxxxxxxxx'
        del data['children'][1]
        response = self.client.post(self.field_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Field.objects.count(), 1)
        self.assertEqual(FieldLink.objects.count(), 0)
        Field.objects.all().delete()
    
    def test_026_create_field_with_null_text_before(self):
        data = self.field_data.copy()
        subfield1 = Field.objects.create(name='Subfield 1')
        data['children'][0]['subfield'] = subfield1.pk
        data['children'][0]['text_before'] = None
        del data['children'][1]
        response = self.client.post(self.field_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Field.objects.count(), 2)
        self.assertEqual(FieldLink.objects.count(), 1)
        FieldLink.objects.all().delete()
        Field.objects.all().delete()

    def test_027_create_field_with_blank_text_before(self):
        data = self.field_data.copy()
        subfield1 = Field.objects.create(name='Subfield 1')
        data['children'][0]['subfield'] = subfield1.pk
        data['children'][0]['text_before'] = ''
        del data['children'][1]
        response = self.client.post(self.field_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Field.objects.count(), 2)
        self.assertEqual(FieldLink.objects.count(), 1)
        FieldLink.objects.all().delete()
        Field.objects.all().delete()

    def test_028_create_field_with_space_in_text_before(self):
        data = self.field_data.copy()
        subfield1 = Field.objects.create(name='Subfield 1')
        data['children'][0]['subfield'] = subfield1.pk
        data['children'][0]['text_before'] = ' '
        del data['children'][1]
        response = self.client.post(self.field_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Field.objects.count(), 2)
        self.assertEqual(FieldLink.objects.count(), 1)
        FieldLink.objects.all().delete()
        Field.objects.all().delete()

    def test_029_create_field_with_duplicated_text_before_to_same_fields(self):
        data = self.field_data.copy()
        subfield1 = Field.objects.create(name='Subfield 1')
        subfield2 = Field.objects.create(name='Subfield 2')
        data['children'][0]['subfield'] = subfield1.pk
        data['children'][0]['text_before'] = 'same text'
        data['children'][1]['subfield'] = subfield2.pk
        data['children'][1]['text_before'] = 'same text'
        response = self.client.post(self.field_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Field.objects.count(), 3)
        self.assertEqual(FieldLink.objects.count(), 2)
        FieldLink.objects.all().delete()
        Field.objects.all().delete()
    
    def test_030_create_field_with_duplicated_text_before_to_different_fields(self):
        data = self.field_data.copy()
        subfield1 = Field.objects.create(name='Subfield 1')
        subfield2 = Field.objects.create(name='Subfield 2')
        subfield3 = Field.objects.create(name='Subfield 3')
        FieldLink.objects.create(
            field=subfield1, subfield=subfield2, sequence=1, text_before='same text'
        )
        data['children'][0]['subfield'] = subfield3.pk
        data['children'][0]['text_before'] = 'same text'
        del data['children'][1]
        response = self.client.post(self.field_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Field.objects.count(), 4)
        self.assertEqual(FieldLink.objects.count(), 2)
        FieldLink.objects.all().delete()
        Field.objects.all().delete()

    # children.text_after
    def test_031_create_field_with_text_after(self):
        data = self.field_data.copy()
        subfield1 = Field.objects.create(name='Subfield 1')
        data['children'][0]['subfield'] = subfield1.pk
        data['children'][0]['text_after'] = 'test_after'
        del data['children'][1]
        response = self.client.post(self.field_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Field.objects.count(), 2)
        self.assertEqual(FieldLink.objects.count(), 1)
        FieldLink.objects.all().delete()
        Field.objects.all().delete()

    def test_032_create_field_with_33_char_in_text_after(self):
        data = self.field_data.copy()
        subfield1 = Field.objects.create(name='Subfield 1')
        data['children'][0]['subfield'] = subfield1.pk
        data['children'][0]['text_after'] = 'less than 32 char xxxxxxxxxxxxxxx'
        del data['children'][1]
        response = self.client.post(self.field_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Field.objects.count(), 1)
        self.assertEqual(FieldLink.objects.count(), 0)
        Field.objects.all().delete()
    
    def test_033_create_field_with_null_text_after(self):
        data = self.field_data.copy()
        subfield1 = Field.objects.create(name='Subfield 1')
        data['children'][0]['subfield'] = subfield1.pk
        data['children'][0]['text_after'] = None
        del data['children'][1]
        response = self.client.post(self.field_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Field.objects.count(), 2)
        self.assertEqual(FieldLink.objects.count(), 1)
        FieldLink.objects.all().delete()
        Field.objects.all().delete()

    def test_034_create_field_with_blank_text_after(self):
        data = self.field_data.copy()
        subfield1 = Field.objects.create(name='Subfield 1')
        data['children'][0]['subfield'] = subfield1.pk
        data['children'][0]['text_after'] = ''
        del data['children'][1]
        response = self.client.post(self.field_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Field.objects.count(), 2)
        self.assertEqual(FieldLink.objects.count(), 1)
        FieldLink.objects.all().delete()
        Field.objects.all().delete()

    def test_035_create_field_with_space_in_text_after(self):
        data = self.field_data.copy()
        subfield1 = Field.objects.create(name='Subfield 1')
        data['children'][0]['subfield'] = subfield1.pk
        data['children'][0]['text_after'] = ' '
        del data['children'][1]
        response = self.client.post(self.field_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Field.objects.count(), 2)
        self.assertEqual(FieldLink.objects.count(), 1)
        FieldLink.objects.all().delete()
        Field.objects.all().delete()

    def test_36_create_field_with_duplicated_text_after_to_same_fields(self):
        data = self.field_data.copy()
        subfield1 = Field.objects.create(name='Subfield 1')
        subfield2 = Field.objects.create(name='Subfield 2')
        data['children'][0]['subfield'] = subfield1.pk
        data['children'][0]['text_after'] = 'same text'
        data['children'][1]['subfield'] = subfield2.pk
        data['children'][1]['text_after'] = 'same text'
        response = self.client.post(self.field_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Field.objects.count(), 3)
        self.assertEqual(FieldLink.objects.count(), 2)
        FieldLink.objects.all().delete()
        Field.objects.all().delete()
    
    def test_037_create_field_with_duplicated_text_after_to_different_fields(self):
        data = self.field_data.copy()
        subfield1 = Field.objects.create(name='Subfield 1')
        subfield2 = Field.objects.create(name='Subfield 2')
        subfield3 = Field.objects.create(name='Subfield 3')
        FieldLink.objects.create(
            field=subfield1, subfield=subfield2, sequence=1, text_after='same text'
        )
        data['children'][0]['subfield'] = subfield3.pk
        data['children'][0]['text_after'] = 'same text'
        del data['children'][1]
        response = self.client.post(self.field_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Field.objects.count(), 4)
        self.assertEqual(FieldLink.objects.count(), 2)
        FieldLink.objects.all().delete()
        Field.objects.all().delete()

    # get
    def test_038_list_fields(self):
        field1 = Field.objects.create(name='field 1')
        field2 = Field.objects.create(name='field 2')
        field3 = Field.objects.create(name='field 3')
        field4 = Field.objects.create(name='field 4')
        field5 = Field.objects.create(name='field 5')
        field6 = Field.objects.create(name='field 6')
        field7 = Field.objects.create(name='field 7')
        link1 = FieldLink.objects.create(field=field1, subfield=field2, sequence=1)
        link2 = FieldLink.objects.create(field=field1, subfield=field3, sequence=2)
        link3 = FieldLink.objects.create(field=field2, subfield=field4, sequence=1)
        link4 = FieldLink.objects.create(field=field2, subfield=field5, sequence=2)
        link5 = FieldLink.objects.create(field=field3, subfield=field6, sequence=1)
        link6 = FieldLink.objects.create(field=field6, subfield=field7, sequence=1)
        response = self.client.get(self.field_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        print(response.data)

        expect = [
            {
                'id': field1.pk,
                'name': field1.name,
                'children': [
                    {
                        'id': link1.pk, 
                        'subfield': field2.pk, 
                        'sequence': link1.sequence,
                        'text_before': None,
                        'text_after': None
                    },
                    {
                        'id': link2.pk, 
                        'subfield': field3.pk, 
                        'sequence': link2.sequence,
                        'text_before': None,
                        'text_after': None
                    },
                ]
            },
            {
                'id': field2.pk,
                'name': field2.name,
                'children': [
                    {
                        'id': link3.pk, 
                        'subfield': field4.pk, 
                        'sequence': link3.sequence,
                        'text_before': None,
                        'text_after': None
                    },
                    {
                        'id': link4.pk, 
                        'subfield': field5.pk, 
                        'sequence': link4.sequence,
                        'text_before': None,
                        'text_after': None
                    },
                ]
            },
            {
                'id': field3.pk,
                'name': field3.name,
                'children': [
                    {
                        'id': link5.pk, 
                        'subfield': field6.pk, 
                        'sequence': link5.sequence,
                        'text_before': None,
                        'text_after': None
                    }
                ]
            },
            {
                'id': field4.pk,
                'name': field4.name,
                'children': []
            },
            {
                'id': field5.pk,
                'name': field5.name,
                'children': []
            },
            {
                'id': field6.pk,
                'name': field6.name,
                'children': [
                    {
                        'id': link6.pk, 
                        'subfield': field7.pk, 
                        'sequence': link6.sequence,
                        'text_before': None,
                        'text_after': None
                    }
                ]
            },
            {
                'id': field7.pk,
                'name': field7.name,
                'children': []
            }
        ]
        self.assertEqual(expect, response.data)
        FieldLink.objects.all().delete()
        Field.objects.all().delete()
