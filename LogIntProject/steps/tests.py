from django.utils import timezone
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch

from sources.models import Source
from .models import Steps
from home.models import Integration
from .views import *

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
        
class StepsModelTestCase(TestCase):
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
            action='TYPE IN',
            img='example.jpg',
            input_value='Test Value',
            integration=self.integration
        )

    def test_str_method(self):
        expected_str = f"Step number: {self.step.step_number} - action: {self.step.action}"
        self.assertEqual(str(self.step), expected_str)

    def test_change_img_name_method(self):
        filename = 'example.jpg'
        expected_new_filename = f"{self.integration.pk}_{self.step.step_number}_{self.step.action}.jpg"
        new_filename = self.step.change_img_name(filename)
        self.assertEqual(new_filename, expected_new_filename)
        
class AddStepTestCase(TestCase):
    def test_add_step(self):
        self.source = Source.objects.create(
            source_name='Test Source', link='http://testsource.com')

        self.integration = Integration.objects.create(
            pk=-100,
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

        request = HttpRequest()
        request.method = 'POST'
        request.POST['integration_id'] = self.integration.pk
        request.POST['action'] = 'TYP'
        request.POST['input_value'] = 'Test Input Value'

        image_data = b'fake image data'
        image_file = SimpleUploadedFile('test_image.png', image_data, content_type='image/png')
        request.FILES['screenshot'] = image_file

        with patch('steps.views.redirect') as mock_redirect:
            response = add_step(request, integration_id=self.integration.pk)
            
        self.assertEqual(response, mock_redirect.return_value)
        self.assertEqual(Steps.objects.count(), 1)
        step = Steps.objects.first()
        self.assertEqual(step.integration, self.integration)
        self.assertEqual(step.step_number, 1)
        self.assertEqual(step.action, 'TYP')
        self.assertEqual(step.input_value, 'Test Input Value')
        self.assertTrue(step.img)
        
        if step.img:
            img_path = os.path.join(settings.MEDIA_ROOT, str(step.img))
            if os.path.exists(img_path):
                os.remove(img_path)
        
class EditStepTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.source = Source.objects.create(source_name='Test Source', link='http://testsource.com')
        self.integration = Integration.objects.create(
            pk = 1,
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
            action='TYP',
            img = 'example.jpg',
            input_value='Test input value',
            integration=self.integration
        )

    def test_edit_step(self):
        url = reverse('edit_step', kwargs={'integration_id': 1})
        data = {
            'step_pk': self.step.pk,
            'step_action': 'TYP',
            'step_img': None,
            'step_input_value': 'Updated input value'
        }
        request = HttpRequest()
        request.method = 'POST'
        request.POST = data
        request.FILES = data

        response = edit_step(request, integration_id=1)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Steps.objects.count(), 1)

        updated_step = Steps.objects.get(pk=self.step.pk)
        self.assertEqual(updated_step.action, 'TYP')
        self.assertEqual(updated_step.input_value, 'Updated input value')
        self.assertIsNotNone(updated_step.img)
