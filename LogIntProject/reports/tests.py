from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
import pytz
from history.models import History
from .views import generate_pdf, generate_txt

class HistoryTestCase(TestCase):
    def setUp(self):
        self.history1 = History.objects.create(
            type='Type1', 
            name='Name1', 
            operation='Operation1', 
            operation_date=timezone.now().astimezone(pytz.timezone('Europe/Warsaw'))
            )
        self.history2 = History.objects.create(
            type='Type2', 
            name='Name2', 
            operation='Operation2', 
            operation_date=timezone.now().astimezone(pytz.timezone('Europe/Warsaw'))
        )

    def test_generate_pdf(self):
        histories = History.objects.all()
        buffer = generate_pdf(histories)
        self.assertTrue(len(buffer.getvalue()) > 0)

    def test_generate_txt(self):
        histories = History.objects.all()
        buffer = generate_txt(histories)
        self.assertTrue(len(buffer.getvalue()) > 0)

class ReportsViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse('all_reports')

    def test_get_all_reports(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')