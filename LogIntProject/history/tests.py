from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.test import TestCase, Client
from .models import History
from django.utils import timezone

class HistoryUnitTestCase(TestCase):

    def test_str_method(self):
        expected_str = f"{self.history.type} | {self.history.name} | {self.history.operation}"
        self.assertEqual(str(self.history), expected_str)
    
    def setUp(self):
        self.factory = RequestFactory()
        self.history = History.objects.create(
            type='Test Type 1',
            name='Test Name 1',
            operation='Test Operation 1',
            operation_date=timezone.now()
        )

    def test_history_creation(self):
        History.objects.create(
            type='Test Type',
            name='Test Name',
            operation='Test Operation',
            operation_date=timezone.now()
        )

        created_history = History.objects.get(type='Test Type')

        self.assertEqual(created_history.name, 'Test Name')
        self.assertEqual(created_history.operation, 'Test Operation')
        
    def test_history_editing(self):
        self.history.name = 'Updated Name'
        self.history.operation = 'Updated Operation'
        self.history.save()

        updated_history = History.objects.get(pk=self.history.pk)

        self.assertEqual(updated_history.name, 'Updated Name')
        self.assertEqual(updated_history.operation, 'Updated Operation')

    def test_history_deletion(self):
        self.history.delete()

        with self.assertRaises(History.DoesNotExist):
            History.objects.get(pk=self.history.pk)
            
class HistoryIntegrationTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        for i in range(20):
            History.objects.create(
                type=f'Test Type {i}',
                name=f'Test Name {i}',
                operation=f'Test Operation {i}',
                operation_date=timezone.now()
            )

    def test_history_view(self):
        url = reverse('history')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/history.html')
        
        paginator = response.context['historys']
        self.assertEqual(len(paginator.object_list), 15)

        response = self.client.get(url, {'page': 2})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/history.html')
        
        paginator = response.context['historys']
        self.assertEqual(len(paginator.object_list), 5)

    def test_empty_history_view(self):
        History.objects.all().delete()

        url = reverse('history')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/history.html')
        
        paginator = response.context['historys']
        self.assertEqual(len(paginator.object_list), 0)