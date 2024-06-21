from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from .models import *
from .views import *
from django.utils import timezone
from django.test import TestCase, Client
from django.conf import settings
from sources.models import Source
from history.models import History

class IntegrationUnitTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='testpassword')
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
        
        self.integration_account = Integration_Account.objects.create(
            driver_id=10,
            login="test_login",
            password="test_password",
            integration=self.integration
        )
    
    def test_str_method(self):
        self.assertEqual(str(self.integration), self.integration.integration_name)

    def test_add_integration_view(self):
        url = reverse('integration')
        request = self.factory.post(url, {
            'integration_name': 'Test Integration 2',
            'app_name': 'Test App 2',
            'source': self.source.source_name,
            'type': 'Test Type 2',
            'customer': 'Test Customer 2',
            'apk_file': 'Test APK File 2',
            'sh_script': 'Test SH Script 2'
        })
        request.user = self.user
        response = add_integration(request)
        self.assertEqual(response.status_code, 302)

    def test_integration_details_view(self):
        url = reverse('integration_details', args=[self.integration.id])
        request = self.factory.get(url)
        request.user = self.user
        response = integration_details(request, self.integration.id)
        self.assertEqual(response.status_code, 200)

    def test_edit_integration_view(self):
        url = reverse('edit_integration', args=[self.integration.id])
        request = self.factory.post(url, {
            'integration_id': self.integration.pk,
            'integration_name': 'Updated Integration Name',
            'app_name': 'Updated App Name',
            'source': self.source.source_name,
            'type': 'Updated Type',
            'customer': 'Updated Customer',
            'apk_file': 'Updated APK File',
            'sh_script': 'Updated SH Script'
        })
        request.user = self.user
        response = edit_integration(request, self.integration.pk)
        self.assertEqual(response.status_code, 302)

    def test_delete_integration_view(self):
        url = reverse('delete_integration', args=[self.integration.pk])
        request = self.factory.post(url)
        request.user = self.user
        response = delete_integration(request, self.integration.pk)
        self.assertEqual(response.status_code, 302)

    def test_add_driver_account_view(self):
        url = reverse('add_driver', args=[self.integration.pk])
        request = self.factory.post(url, {
            'driver_id': 1,
            'driver_login': 'test_driver_login',
            'driver_password': 'test_driver_password'
        })
        request.user = self.user
        response = add_driver_account(request, self.integration.pk)
        self.assertEqual(response.status_code, 302)

    def test_edit_driver_account_with_new_password(self):
        response = self.client.post(reverse('edit_driver', args=[self.integration.pk]), {
            'primary_id': self.integration_account.pk,
            'driver_id': self.integration_account.driver_id,
            'driver_login': 'test_login',
            'driver_password': 'test_password',
            'driver_new_password': 'new_password'
        })
        
        self.integration_account.refresh_from_db()
        self.assertEqual(self.integration_account.password, 'new_password')
        self.assertTrue(History.objects.filter(name='test_login', operation='Edited').exists())
        self.assertRedirects(response, f'/home/integration{self.integration.pk}')
    
    def test_edit_driver_account_without_new_password(self):
        response = self.client.post(reverse('edit_driver', args=[self.integration.pk]), {
            'primary_id': self.integration_account.pk,
            'driver_id': self.integration_account.driver_id,
            'driver_login': 'test_login',
            'driver_password': 'test_password',
            'driver_new_password': ''
        })
        
        self.integration_account.refresh_from_db()
        self.assertEqual(self.integration_account.password, 'test_password')
        self.assertTrue(History.objects.filter(name='test_login', operation='Edited').exists())
        self.assertRedirects(response, f'/home/integration{self.integration.pk}')


    def test_delete_driver_account_view(self):
        integration_account = Integration_Account.objects.create(
            driver_id=1, login='test_driver_login', password='test_driver_password', integration=self.integration)
        url = reverse('delete_driver', args=[self.integration.id])
        request = self.factory.post(url, {
            'driver_id': integration_account.driver_id,
            'driver_login': integration_account.login,
            'integration_id': self.integration.pk
        })
        request.user = self.user
        response = delete_driver_account(request, self.integration.pk)
        self.assertEqual(response.status_code, 302)

    def test_home_delete_integration_view(self):
        integration2 = Integration.objects.create(
            integration_name='Test Integration 2',
            app_name='Test App 2',
            customer='Test Customer 2',
            source=self.source,
            type='Test Type 2',
            apk_file='Test APK File 2',
            sh_script='Test SH Script 2',
            is_active=True,
            integration_date=timezone.now()
        )
        url = reverse('home_delete_integration')
        request = self.factory.post(url, {'integration_pks': [self.integration.pk, integration2.pk]})
        request.user = self.user
        response = home_delete_integration(request)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Integration.objects.filter(pk=self.integration.pk).exists())
        self.assertFalse(Integration.objects.filter(pk=integration2.pk).exists())
        
    def test_activate_integration(self):
        url = reverse('activate_deactivate_integration', args=[self.integration.pk, 'Activated'])
        request = self.factory.get(url)
        request.user = self.user
        response = activate_deactivate_integration(request, self.integration.pk, 'Activated')
        self.assertEqual(response.status_code, 302)
        self.integration.refresh_from_db()
        self.assertTrue(self.integration.is_active)

    def test_deactivate_integration(self):
        url = reverse('activate_deactivate_integration', args=[self.integration.pk, 'Deactivate'])
        request = self.factory.get(url)
        request.user = self.user
        response = activate_deactivate_integration(request, self.integration.pk, 'Deactivate')
        self.assertEqual(response.status_code, 302)
        self.integration.refresh_from_db()
        self.assertFalse(self.integration.is_active)
        

class IntegrationFunctionalityTestCase(TestCase):

    def setUp(self):
        self.client = Client()
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
        self.integration_account = Integration_Account.objects.create(
            driver_id=1,
            login='test_driver_login',
            password='test_driver_password',
            integration=self.integration
        )

    def test_add_integration(self):
        url = reverse('integration')
        data = {
            'integration_name': 'New Integration',
            'app_name': 'New App',
            'source': self.source.pk,
            'type': 'New Type',
            'customer': 'New Customer',
            'apk_file': 'New APK File',
            'sh_script': 'New SH Script'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful addition
        self.assertTrue(Integration.objects.filter(integration_name='New Integration').exists())
        self.assertTrue(History.objects.filter(name='New Integration', operation='Added').exists())

    def test_integration_details(self):
        url = reverse('integration_details', args=[self.integration.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # Success status
        self.assertTemplateUsed(response, 'pages/integration_details.html')

    def test_edit_integration(self):
        url = reverse('edit_integration', args=[self.integration.pk])
        data = {
            'integration_id': self.integration.pk,
            'integration_name': 'Updated Integration Name',
            'app_name': 'Updated App Name',
            'source': self.source.pk,
            'type': 'Updated Type',
            'customer': 'Updated Customer',
            'apk_file': 'Updated APK File',
            'sh_script': 'Updated SH Script'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful edition
        self.integration.refresh_from_db()
        self.assertEqual(self.integration.integration_name, 'Updated Integration Name')
        self.assertTrue(History.objects.filter(name='Updated Integration Name', operation='Edited').exists())

    def test_delete_integration(self):
        url = reverse('delete_integration', args=[self.integration.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        self.assertFalse(Integration.objects.filter(pk=self.integration.pk).exists())
        self.assertTrue(History.objects.filter(name='Test Integration', operation='Deleted').exists())

    def test_add_driver_account(self):
        url = reverse('add_driver', args=[self.integration.pk])
        data = {
            'driver_id': 2,
            'driver_login': 'New Driver Login',
            'driver_password': 'New Driver Password'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Integration_Account.objects.filter(login='New Driver Login').exists())
        self.assertTrue(History.objects.filter(name='New Driver Login', operation='Added').exists())

    def test_edit_driver_account(self):
        url = reverse('edit_driver', args=[self.integration.pk])
        data = {
            'primary_id': self.integration_account.pk,
            'driver_id': 3,
            'driver_login': 'Updated Driver Login',
            'driver_password': 'Updated Driver Password',
            'driver_new_password': ''
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful edition
        self.integration_account.refresh_from_db()
        self.assertEqual(self.integration_account.login, 'Updated Driver Login')
        self.assertTrue(History.objects.filter(name='Updated Driver Login', operation='Edited').exists())

    def test_delete_driver_account(self):
        url = reverse('delete_driver', args=[self.integration.pk])
        data = {
            'driver_id': self.integration_account.driver_id,
            'driver_login': self.integration_account.login,
            'integration_id': self.integration.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        self.assertFalse(Integration_Account.objects.filter(pk=self.integration_account.pk).exists())
        self.assertTrue(History.objects.filter(name='test_driver_login', operation='Deleted').exists())

class IntegrationAccountTestCase(TestCase):

    def setUp(self):

        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='testpassword')
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
        
        self.integration_account = Integration_Account.objects.create(
            driver_id=10,
            login="test_login",
            password="test_password",
            integration=self.integration
        )
        
    def test_str_method(self):
        self.assertEqual(str(self.integration_account), self.integration_account.login)

class PasswordEncryptionTest(TestCase):
    def setUp(self):
        self.encryption_key = settings.ENCRYPTION_KEY

    def test_encrypt_password(self):
        password = "mysecretpassword"
        encrypted_password = encrypt_password(password)
        self.assertNotEqual(encrypted_password, password.encode('utf-8'))
        decrypted_password = decrypt_password(encrypted_password)
        self.assertEqual(decrypted_password, password)

    def test_decrypt_password(self):
        password = "mysecretpassword"
        encrypted_password = encrypt_password(password)
        decrypted_password = decrypt_password(encrypted_password)
        self.assertEqual(decrypted_password, password)

    def test_encrypt_decrypt_password(self):
        password = "mysecretpassword"
        encrypted_password = encrypt_password(password)
        decrypted_password = decrypt_password(encrypted_password)
        self.assertEqual(decrypted_password, password)
        self.assertNotEqual(encrypted_password, password.encode('utf-8'))
        
class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.source1 = Source.objects.create(source_name="Source 1")
        self.source2 = Source.objects.create(source_name="Source 2")
        self.integration1 = Integration.objects.create(
            integration_name="Integration 1",
            app_name="App 1",
            customer="Customer 1",
            source=self.source1,
            type="Type 1",
            apk_file="path/to/apk1",
            sh_script="path/to/script1",
            is_active=True,
            integration_date=timezone.now()
        )
        
        self.integration2 = Integration.objects.create(
            integration_name="Integration 2",
            app_name="App 2",
            customer="Customer 2",
            source=self.source2,
            type="Type 2",
            apk_file="path/to/apk2",
            sh_script="path/to/script2",
            is_active=False,
            integration_date=timezone.now()
        )
    
    def test_home_view_active_integrations(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.integration1, response.context['integrations'])
        self.assertNotIn(self.integration2, response.context['integrations'])
    
    def test_home_view_inactive_integrations(self):
        response = self.client.get(reverse('home'), {'show_inactive': 'true'})
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.integration1, response.context['integrations'])
        self.assertIn(self.integration2, response.context['integrations'])
    
    def test_home_view_pagination(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['integrations']), 1)  # Assuming pagination size is 4 and there are only 2 items
    
    def test_home_view_source_choices(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['source_choices'], {self.source1.source_name: self.source1.source_name, self.source2.source_name: self.source2.source_name})
    
    def test_home_view_type_choices(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['type_choices'], type_choices)