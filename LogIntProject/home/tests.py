from django.test import TestCase
from .models import Integration

class IntegrationModelTestCase(TestCase):
    def setUp(self):
        self.integration = Integration.objects.create(
            integration_name='Test Integration',
            customer='Test Customer',
            driver_id=123,
            source='Test Source',
            apk_file='test.apk',
            sh_script='test.sh',
            is_active=True
        )

    #  Test if variable are correctly assigned
    def test_integration_creation(self):
        self.assertEqual(self.integration.integration_name, 'Test Integration')
        self.assertEqual(self.integration.customer, 'Test Customer')
        self.assertEqual(self.integration.driver_id, 123)
        self.assertEqual(self.integration.source, 'Test Source')
        self.assertEqual(self.integration.apk_file, 'test.apk')
        self.assertEqual(self.integration.sh_script, 'test.sh')
        self.assertTrue(self.integration.is_active)

    # Test for function returning its own name in database
    def test_string_representation(self):
        self.assertEqual(str(self.integration), 'Test Integration')

    # Test if blank is_active is set to True by default
    def test_default_is_active(self):
        new_integration = Integration.objects.create(
            integration_name='New Test Integration',
            customer='New Test Customer',
            driver_id=456,
            source='New Test Source',
            apk_file='new_test.apk',
            sh_script='new_test.sh'
        )
        self.assertTrue(new_integration.is_active)

    # Test for blank fields (except for is_active which has a default value)
    def test_blank_fields(self):
        blank_integration = Integration.objects.create(
            integration_name='',
            customer='',
            driver_id=0,
            source='',
            apk_file='',
            sh_script=''
        )
        self.assertEqual(blank_integration.integration_name, '')
        self.assertEqual(blank_integration.customer, '')
        self.assertEqual(blank_integration.driver_id, 0)
        self.assertEqual(blank_integration.source, '')
        self.assertEqual(blank_integration.apk_file, '')
        self.assertEqual(blank_integration.sh_script, '')
        self.assertTrue(blank_integration.is_active)  # should default to True
