from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.template.loader import render_to_string

from .views import emulator

class EmulatorViewTestCase(TestCase):
    def test_emulator_view(self):
        request = RequestFactory().get(reverse('emulator'))
        response = emulator(request)
        self.assertEqual(response.status_code, 200)
        expected_html = render_to_string('pages/emulator.html')
        self.assertHTMLEqual(response.content.decode(), expected_html)