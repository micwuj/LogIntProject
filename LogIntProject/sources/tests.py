from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.test import Client
from home.models import Integration
from history.models import History
from sources.models import Source

class SourceUnitTestCase(TestCase):
    def test_source_creation(self):
        source = Source.objects.create(
            source_name='Test Source',
            link='http://example.com'
        )
        self.assertEqual(Source.objects.count(), 1)
        self.assertEqual(source.source_name, 'Test Source')
    
    def setUp(self):
        self.factory = RequestFactory()

    def test_sources_view(self):
        url = reverse('sources')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/sources.html')

    def test_add_source_view(self):
        url = reverse('add_source')
        data = {'source_name': 'New Source', 'link': 'http://example.com'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Source.objects.filter(source_name='New Source').exists())
        self.assertTrue(History.objects.filter(name='New Source', operation='Added').exists())

    def test_edit_source_view(self):
        Source.objects.create(source_name='Old Source', link='http://oldsource.com')
        url = reverse('edit_source')
        data = {'previous_source_name': 'Old Source', 'source_name': 'New Source', 'link': 'http://newsource.com'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(History.objects.filter(name='New Source', operation='Edited').exists())

    def test_delete_source_view(self):
        Source.objects.create(source_name='Test Source', link='http://testsource.com')
        url = reverse('delete_source')
        data = {'source_names': ['Test Source']}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Source.objects.filter(source_name='Test Source').exists())
        self.assertTrue(History.objects.filter(name='Test Source', operation='Deleted').exists())


class SourceIntegrationTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_add_source_view(self):
        url = reverse('add_source')

        # Simulate a GET request (invalid request)
        response = self.client.get(url)

        # Assert that the response contains the expected JSON data
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'error': 'Invalid request'})

        # Now, simulate a POST request (valid request)
        data = {
            'source_name': 'Test Source',
            'link': 'http://example.com'
        }
        response = self.client.post(url, data)

        # Assert that the response contains the expected JSON data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Source.objects.count(), 1)
        self.assertEqual(Source.objects.first().source_name, 'Test Source')

    def test_edit_source_view(self):
        source = Source.objects.create(
            source_name='Test Source',
            link='http://example.com'
        )

        url = reverse('edit_source')
        data = {
            'previous_source_name': 'Test Source',
            'source_name': 'Test Source',
            'link': 'http://updatedsource.com'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Source.objects.first().link, 'http://updatedsource.com')

        history = History.objects.get(name='Test Source', operation='Edited')
        self.assertEqual(history.operation, 'Edited')

    def test_edit_source_name_exists_view(self):
        Source.objects.create(source_name='Existing Source', link='http://existingsource.com')

        url = reverse('edit_source')
        data = {
            'previous_source_name': 'Test Source',
            'source_name': 'Existing Source',
            'link': 'http://updatedsource.com'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'error': 'Source with this name already exists'})

    def test_edit_source_not_found_view(self):
        url = reverse('edit_source')
        data = {
            'previous_source_name': 'Nonexistent Source',
            'source_name': 'Updated Source',
            'link': 'http://updatedsource.com'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(response.content, {'error': 'Source not found'})

    def test_delete_source_view(self):
        Source.objects.create(source_name='Another Source', link='http://anothersource.com')

        url = reverse('delete_source')
        data = {'source_names': ['Test Source', 'Another Source']}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Source.objects.filter(source_name='Test Source').exists())
        self.assertFalse(Source.objects.filter(source_name='Another Source').exists())
        self.assertFalse(Integration.objects.filter(source__source_name='Test Source').exists())

        history1 = History.objects.get(name='Test Source')
        self.assertEqual(history1.operation, 'Deleted')

        history2 = History.objects.get(name='Another Source')
        self.assertEqual(history2.operation, 'Deleted')

