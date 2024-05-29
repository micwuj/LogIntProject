from django.test import TestCase
from .models import Integration, Integration_Account
from sources.models import Source
from datetime import datetime
from unittest.mock import patch, Mock, mock_open
import json
from home.tasks import pull_data_from_active_resources_scheduled

class IntegrationModelTest(TestCase):

    def setUp(self):
        self.source = Source.objects.create(
            source_name = 'Test Source',
            link = 'http://example.com'
        )
        # Create a sample Integration instance
        self.integration = Integration.objects.create(
            integration_name='Test Integration',
            app_name='Test App',
            customer='Test Customer',
            source=self.source,
            type='Test Type',
            apk_file='Test APK File',
            sh_script='Test SH Script',
            is_active=True,
            integration_date=datetime.now()
        )

        # Create a sample Integration_Account instance
        self.integration_account = Integration_Account.objects.create(
            driver_id=1,
            login='test_login',
            password='test_password',
            integration=self.integration
        )

    def test_integration_creation(self):
        integration = Integration.objects.get(integration_name='Test Integration')
        self.assertEqual(integration.app_name, 'Test App')
        self.assertEqual(integration.customer, 'Test Customer')

    def test_integration_editing(self):
        integration = Integration.objects.get(integration_name='Test Integration')
        integration.app_name = 'Updated App Name'
        integration.save()
        updated_integration = Integration.objects.get(integration_name='Test Integration')
        self.assertEqual(updated_integration.app_name, 'Updated App Name')

    def test_integration_deleting(self):
        integration = Integration.objects.get(integration_name='Test Integration')
        integration.delete()
        self.assertFalse(Integration.objects.filter(integration_name='Test Integration').exists())

    def test_integration_account_creation(self):
        integration_account = Integration_Account.objects.get(login='test_login')
        self.assertEqual(integration_account.driver_id, 1)
        self.assertEqual(integration_account.password, 'test_password')

    def test_integration_account_editing(self):
        integration_account = Integration_Account.objects.get(login='test_login')
        integration_account.password = 'updated_password'
        integration_account.save()
        updated_account = Integration_Account.objects.get(login='test_login')
        self.assertEqual(updated_account.password, 'updated_password')

    def test_integration_account_deleting(self):
        integration_account = Integration_Account.objects.get(login='test_login')
        integration_account.delete()
        self.assertFalse(Integration_Account.objects.filter(login='test_login').exists())