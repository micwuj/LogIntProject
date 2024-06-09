from django.utils import timezone
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from sources.models import Source
from .models import Steps
from home.models import Integration

class StepUnitTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.source = Source.objects.create(
            source_name='Test Source', link='http://testsource.com')
        self.integration = Integration.objects.create(
            integration_name='Test Integration',
            app_name='Test App',
            customer='Test Customer',
            source=self.source,
            type='Test Type',
            apk_file='Test APK File',
            sh_script='Test SH Script',
            is_active=True,
            integration_date=timezone.now()
        )
        self.client = Client()
        self.client.login(username='testuser', password='12345')
        self.step = Steps.objects.create(
            step_number=1,
            action='TYP',
            input_value='Test input value',
            integration=self.integration
        )
    def test_delete_step(self):
        response = self.client.post(reverse('delete_step', kwargs={'integration_id': self.integration.pk}), {
            'step_pk': self.step.pk
        })
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Steps.objects.filter(pk=self.step.pk).exists())

class StepIntegrityTestCase(TestCase):
    def setUp(self):
        self.source = Source.objects.create(
            source_name='Test Source', link='http://testsource.com')
        self.integration = Integration.objects.create(
            integration_name='Test Integration',
            app_name='Test App',
            customer='Test Customer',
            source=self.source,
            type='Test Type',
            apk_file='Test APK File',
            sh_script='Test SH Script',
            is_active=True,
            integration_date=timezone.now()
        )
        self.step = Steps.objects.create(
            step_number=1,
            action="Typ",
            input_value="Test Input",
            integration=self.integration
        )

    def test_step_relationship_integrity(self):
        self.assertEqual(self.step.integration, self.integration)

    def test_step_deletion_cascades(self):
        self.integration.delete()
        self.assertFalse(Steps.objects.filter(pk=self.step.pk).exists())