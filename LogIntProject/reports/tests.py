from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.utils import timezone
import pytz
from history.models import History
from .views import *
from unittest.mock import MagicMock
from reportlab.lib.units import inch

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

class TestAddPageNumber(TestCase):
    def test_add_page_number(self):
        canvas_mock = MagicMock()
        canvas_mock.getPageNumber.return_value = 5
        add_page_number(canvas_mock, None)
        
        canvas_mock.drawRightString.assert_called_once_with(200 * inch, 20 * inch, "Page 5")
        
class ReportsViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.url = reverse('all_reports')

    def test_get_all_reports(self):
        request = self.factory.post(self.url)
        response = get_all_reports(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        
class ReportsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.url = reverse('reports')

    def test_reports_post_with_parameters(self):
        date_from = '2023-01-01'
        date_to = '2023-01-10'
        type_value = 'Type1'
        operation = 'Operation1'
        data = {
            'date_from': date_from,
            'date_to': date_to,
            'type': type_value,
            'operation': operation
        }
        request = self.factory.post(self.url, data=data)
        response = reports(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')

    def test_reports_post_with_date_from_only(self):
        date_from = '2023-01-01'
        data = {
            'date_from': date_from,
        }
        request = self.factory.post(self.url, data=data)
        response = reports(request)
        self.assertEqual(response.status_code, 200)

    def test_reports_post_with_date_to_only(self):
        date_to = '2023-01-10'
        data = {
            'date_to': date_to,
        }
        request = self.factory.post(self.url, data=data)
        response = reports(request)
        self.assertEqual(response.status_code, 200)
        
    def test_reports_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/reports.html')