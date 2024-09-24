from django.test import TestCase
from django.urls import reverse
from ..models import *


URL_NEW = 'post-list-field-relationship'

class NewServicesTestCase(TestCase):

    # def setUp(self):
    #     """
    #     Create users and give the permissions them.
    #     """
    #     self.user = create_user('user')
    #     self.unauthorized= create_user('unauthorized')
    #     self.user.user_permissions.add(get_permission('user'))


    def test_view_field_relationship_post_001(self):
        """
        field == subfield (atomic transaction)
        """
        field1 = Field.objects.create(name='field1')
        field2 = Field.objects.create(name='field2')
        data = [
            {'field': field1.pk, 'subfield': field1.pk, 'sequence': 1}, 
            {'field': field1.pk, 'subfield': field2.pk, 'sequence': 2}
        ]
        request = self.client.post(
            reverse(URL_NEW), data, content_type='application/json'
        )
        self.assertEqual(request.status_code, 400)
        self.assertEqual(FieldLink.objects.all().count(), 0)
        FieldLink.objects.all().delete()


    def test_view_field_relationship_post_002(self):
        """
        duplicated (atomic transaction)
        """
        field1 = Field.objects.create(name='field1')
        field2 = Field.objects.create(name='field2')
        data = [
            {'field': field1.pk, 'subfield': field2.pk, 'sequence': 1}, 
            {'field': field1.pk, 'subfield': field2.pk, 'sequence': 2}
        ]
        request = self.client.post(
            reverse(URL_NEW), data, content_type='application/json'
        )
        self.assertEqual(request.status_code, 400)
        self.assertEqual(FieldLink.objects.all().count(), 0)
        FieldLink.objects.all().delete()
    

    def test_view_field_relationship_post_003(self):
        """
        existing (atomic transaction)
        """
        field1 = Field.objects.create(name='field1')
        field2 = Field.objects.create(name='field2')
        field3 = Field.objects.create(name='field3')
        existing = FieldLink.objects.create(
            field=field1, subfield=field2, sequence=1
        )
        data = [
            {'field': field1.pk, 'subfield': field2.pk, 'sequence': 2},
            {'field': field1.pk, 'subfield': field3.pk, 'sequence': 3}
        ]
        request = self.client.post(
            reverse(URL_NEW), data, content_type='application/json'
        )
        self.assertEqual(request.status_code, 400)
        self.assertEqual(FieldLink.objects.all().count(), 1)
        obj = FieldLink.objects.all().first()
        self.assertEqual(existing, obj)
        FieldLink.objects.all().delete()