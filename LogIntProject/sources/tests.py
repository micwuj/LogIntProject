from django.test import TestCase
from django.urls import reverse
from sources.models import Source

class SourceTestCase(TestCase):
    def test_add_source(self):
        url = reverse('add_source')
        data = {
            'source_name': 'Test Source',
            'link': 'http://example.com'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Source.objects.count(), 1)
        self.assertEqual(Source.objects.first().source_name, 'Test Source')

    def test_edit_source(self):
        source = Source.objects.create(source_name='Initial Name', link='http://initial.com')
        url = reverse('edit_source')
        data = {
            'id': [source.id],
            'source_name': 'Updated Name',
            'link': 'http://updated.com'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        source.refresh_from_db()
        self.assertEqual(source.source_name, 'Updated Name')
        self.assertEqual(source.link, 'http://updated.com')

    def test_delete_source(self):
        source = Source.objects.create(source_name='Delete Me', link='http://delete.com')
        url = reverse('delete_source')
        response = self.client.post(url, {'ids': [source.id]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Source.objects.count(), 0)

