from django.test import TestCase
from django.urls import reverse
from ..models import *


URL_GET = 'list-or-create-many-field'

class NewServicesTestCase(TestCase):

    # def setUp(self):
    #     """
    #     Create users and give the permissions them.
    #     """
    #     self.user = create_user('user')
    #     self.unauthorized= create_user('unauthorized')
    #     self.user.user_permissions.add(get_permission('user'))


    def test_view_field_relationship_get_001(self):
        """
        field == subfield (atomic transaction)
        """
        field1 = Field.objects.create(name='field1')
        field2 = Field.objects.create(name='field2')
        field3 = Field.objects.create(name='field3')
        field4 = Field.objects.create(name='field4')
        field5 = Field.objects.create(name='field5')
        field6 = Field.objects.create(name='field6')
        field7 = Field.objects.create(name='field7')
        link1 = FieldLink.objects.create(field=field1, subfield=field2, sequence=1)
        link2 = FieldLink.objects.create(field=field1, subfield=field3, sequence=2)
        link3 = FieldLink.objects.create(field=field3, subfield=field4, sequence=1)
        link4 = FieldLink.objects.create(field=field3, subfield=field5, sequence=2)
        link5 = FieldLink.objects.create(field=field4, subfield=field6, sequence=1)

        request = self.client.get(reverse(URL_GET))
        self.assertEqual(request.status_code, 200)
        print(request.json())
        expect = [
            {
                'id': field1.pk,
                'name': field1.name,
                'children': [
                    {
                        'id': field2.pk,
                        'name': field2.name,
                        'sequence': link1.sequence,
                        'text_before': "",
                        'text_after': "",
                        'children': []
                    },
                    {
                        'id': field3.pk,
                        'name': field3.name,
                        'sequence': link2.sequence,
                        'text_before': "",
                        'text_after': "",
                        'children': [
                            {
                                'id': field4.pk,
                                'name': field4.name,
                                'sequence': link3.sequence,
                                'text_before': "",
                                'text_after': "",
                                'children': [
                                    {
                                        'id': field6.pk,
                                        'name': field6.name,
                                        'sequence': link4.sequence,
                                        'text_before': "",
                                        'text_after': "",
                                        'children': []
                                    }
                                ]
                            },
                            {
                                'id': field5.pk,
                                'name': field5.name,
                                'sequence': link4.sequence,
                                'text_before': "",
                                'text_after': "",
                                'children': []
                            }
                        ]
                    }
                ]
            },
            {
                'id': field2.pk,
                'name': field2.name,
                'children': []
            },
            {
                'id': field3.pk,
                'name': field3.name,
                'children': [
                    {
                        'id': field4.pk,
                        'name': field4.name,
                        'children': [
                            {
                                'id': field6.pk,
                                'name': field6.name,
                                'children': []
                            }
                        ]
                    },
                    {
                        'id': field5.pk,
                        'name': field5.name,
                        'children': []
                    }
                ]
            },
            {
                'id': field4.pk,
                'name': field4.name,
                'children': [
                    {
                        'id': field6.pk,
                        'name': field6.name,
                        'children': []
                    }
                ]
            },
            {
                'id': field5.pk,
                'name': field5.name,
                'children': []
            },
            {
                'id': field6.pk,
                'name': field6.name,
                'children': []
            },
            {
                'id': field7.pk,
                'name': field7.name,
                'children': []
            }
        ]
        self.assertEqual(request.json(), expect)
        FieldLink.objects.all().delete()