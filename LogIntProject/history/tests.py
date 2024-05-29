from django.test import TestCase, RequestFactory
from django.urls import reverse
from .models import History
from django.utils import timezone

class HistoryViewsTestCase(TestCase):

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